from flask import Flask, request, abort
from urllib.parse import parse_qsl

from events.basic import *
from events.service import *
from line_bot_api import *
from events.admin import *
from extensions import db, migrate
from models.user import User
import os


app = Flask(__name__)
app.config.from_object(os.environ.get("APP_SETTINGS", "config.DevConfig"))
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://tim:jcWp8TX0fAbBDNNJ5yqPRWValFJumLJc@dpg-cjg2p641ja0c739rgr30-a.singapore-postgres.render.com/aigo_owcd"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.app = app
db.init_app(app)
migrate.init_app(app, db)


@app.route("/callback", methods = ['POST'])
def callback():
    signature = request.headers["X-Line-Signature"]

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_text = str(event.message.text).lower()
    user = User.query.filter(User.line_id == event.source.user_id).first()#取得user的第一筆資料
    #如果沒有user的資料時,才會透過api去取得
    if not user:
        profile = line_bot_api.get_profile(event.source.user_id)#line API中說明get_profile可以取得的資料
        print(profile.display_name)
        print(profile.user_id)#相同的好友會因為不同的profile而有不同的user_id
        print(profile.picture_url)

        user = User(profile.user_id, profile.display_name, profile.picture_url)
        db.session.add(user)
        db.session.commit()

    print(user.id)
    print(user.line_id)
    print(user.display_name)


    if message_text == "@關於我們":
        about_us_event(event)

    elif message_text == "@營業據點":
        location_event(event)

    elif message_text == "@預約服務":
        service_category_event(event)
    
    elif message_text.startswith('*'):
        if event.source.user_id not in ['Ua6087f825ae670f8e9303a7efd02519d']:
            return
        if message_text in ['*data', '*d']:
            list_reservation_event(event)
        elif message_text in ['*group', '*g']:
            pass
            # create_audience_group(event)

@handler.add(PostbackEvent)
def handle_postback(event):
    data = dict(parse_qsl(event.postback.data))
    if data.get('action') == 'service':
        service_event(event)
    elif data.get('action') == 'select_date':
        service_select_date_event(event)
    elif data.get('action') == 'select_time':
        service_select_time_event(event)
    elif data.get('action') == 'confirm':
        service_confirm_event(event)
    elif data.get('action') == 'confirmed':
        service_confirmed_event(event)
    elif data.get('action') == 'cancel':
        service_cancel_event(event)
    elif data.get('action') == 'reorder':
        service_category_event(event)

    print('action:', data.get('action'))
    print('category', data.get('category'))
    print('service_id', data.get('service_id'))
    print('date', data.get('date'))
    print('time', data.get('time'))

@handler.add(FollowEvent)
def handle_follow(event):
    welcome_msg = """Hello! 您好，感謝您成為 J髮時尚 的好友！
    
我是 J髮時尚 的小幫手，
我們採個人服務預約優先制，
溫馨放鬆的美髮VIP空間，
每週一固定店休，
每個月最後一週禮拜日公休

-想預約剪/燙/染/洗/護髮服務都可以直接跟我互動喔😊😊~
-直接點選下方【歡迎光臨專屬您的美髮服務】選單功能

-期待您的光臨！"""

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=welcome_msg))

@handler.add(UnfollowEvent)
def handle_unfollow(event):
    print(event)



if __name__ == "__main__":
    app.run()