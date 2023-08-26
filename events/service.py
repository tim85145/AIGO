from line_bot_api import *
from urllib.parse import parse_qsl
import datetime

from extensions import db
from models.user import User
from models.reservation import Reservation  #資料寫入資料庫中


# 預約相關的功能都會寫在這裡，增加多個服務項目
services = {
    1: {
        'category': '按摩調理',
        'img_url': 'https://i.imgur.com/dr03mxX.jpg',
        'title': '按摩調理(指壓/精油)',
        'duration': '90min',
        'description': '深層肌肉緊繃痠痛、工作壓力和緊繃情緒、身體疲勞者，想解除肌肉緊繃僵硬不是感',
        'price': 2000,
        'post_url':'https://linecorp.com'
    },
    2: {
        'category': '按摩調理',
        'img_url': 'https://i.imgur.com/4OMmmI7.png',
        'title': '運動按摩(按摩與伸展)',
        'duration': '90min',
        'description': '全身肌肉按摩放鬆與伸展，能夠改善運動後引發的延遲性痠痛，血液循環流通順暢',
        'price': 1500,
        'post_url':'https://linecorp.com'
    },
    3: {
        'category': '按摩調理',
        'img_url': 'https://i.imgur.com/QeV9g7t.png',
        'title': '熱石精油舒壓',
        'duration': '120min',
        'description': '「火山石」成分含有豐富礦物質及獨特的自然能量，溫熱觸感能活絡循環，鬆解疲勞感，舒緩肌肉緊繃',
        'price': 2000,
        'post_url':'https://linecorp.com'
    },
    4: {
        'category': '臉部護理',
        'img_url': 'https://i.imgur.com/aLFnXu9.png',
        'title': '粉刺淨化 + 深層保濕',
        'duration': '90min',
        'description': '臉部淨化 + 粉刺淨化 + 深層保濕繃',
        'price': 2000,
        'post_url':'https://linecorp.com'
    },
}

def service_category_event(event):
    image_carousel_template_message = TemplateSendMessage(
        alt_text='請選擇想服務類別',
        template=ImageCarouselTemplate(
            columns=[
                ImageCarouselColumn(
                    image_url='https://i.imgur.com/1M87ufu.jpg',
                    action=PostbackAction(
                        label='按摩調理',
                        display_text='想了解按摩調理',
                        data='action=service&category=按摩調理'
                    )
                ),
                ImageCarouselColumn(
                    image_url='https://i.imgur.com/MVk4cTR.jpg',
                    action=PostbackAction(
                        label='臉部護理',
                        display_text='想了解臉部護理',
                        data='action=service&category=臉部護理'
                    )
                )
            ]
        )
    )
    line_bot_api.reply_message(
        event.reply_token,
        [image_carousel_template_message])


def service_event(event):
    data = dict(parse_qsl(event.postback.data))
    bubbles = []

    for service_id in services:
        if services[service_id]['category'] == data['category']:
            service = services[service_id]
            bubble = {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover",
                    "url": service['img_url']
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "text",
                            "text": service['title'],
                            "wrap": True,
                            "weight": "bold",
                            "size": "xl"
                        },
                        {
                            "type": "text",
                            "text": service['duration'],
                            "size": "md",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": service['description'],
                            "margin": "lg",
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": f"NT$ {service['price']}",
                                    "wrap": True,
                                    "weight": "bold",
                                    "size": "xl",
                                    "flex": 0
                                }
                            ],
                            "margin": "xl"
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "action": {
                                "type": "postback",
                                "label": "預約",
                                "data": f"action=select_date&service_id={service_id}",
                                "displayText": f"我想預約【{service['title']} {service['duration']}】"
                            },
                            "color": "#b28530"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "uri",
                                "label": "了解詳情",
                                "uri": service['post_url']
                            }
                        }
                    ]
                }
            }
            
            bubbles.append(bubble)
    
    flex_message = FlexSendMessage(
        alt_text='請選擇預約項目',
        contents={
            "type": "carousel",
            "contents": bubbles
        })

    line_bot_api.reply_message(
        event.reply_token,
        [flex_message])
    

def service_select_date_event(event):
    data = dict(parse_qsl(event.postback.data))

    weekday_string = {
        0: '一',
        1: '二', 
        2: '三',
        3: '四',
        4: '五',
        5: '六',
        6: '日',
    }

    business_day = [1, 2, 3, 4, 5, 6]   #每周上班日

    quick_reply_buttons = []

    today = datetime.datetime.today().date()
    for x in range(1, 11):
        day = today + datetime.timedelta(days=x)

        if day.weekday() in business_day:
            quick_reply_button = QuickReplyButton(
                action=PostbackAction(label=f'{day} ({weekday_string[day.weekday()]})',
                                      text=f'我要預約 {day} ({weekday_string[day.weekday()]}) 這天',
                                      data=f'action=select_time&service_id={data["service_id"]}&date={day}'))
            
            quick_reply_buttons.append(quick_reply_button)

    text_message = TextSendMessage(text='請問要預約哪一天？',
                                   quick_reply=QuickReply(items=quick_reply_buttons))
    line_bot_api.reply_message(
        event.reply_token,
        [text_message])


def service_select_time_event(event):
    data =dict(parse_qsl(event.postback.data))

    available_time = ["11:00", "14:00", "17:00", "20:00"]

    quick_reply_buttons = []

    for time in available_time:
        quick_reply_button = QuickReplyButton(action=PostbackAction(label=time,
                                                                    text=f"{time} 這個時段", 
                                                                    data=f'action=confirm&service_id={data["service_id"]}&date={data["date"]}&time={time}'))
        quick_reply_buttons.append(quick_reply_button)

    text_message = TextSendMessage(text='請問要預約哪個時段？',
                                   quick_reply=QuickReply(items=quick_reply_buttons))
    line_bot_api.reply_message(
        event.reply_token,
        [text_message])
    

def service_confirm_event(event):
    data = dict(parse_qsl(event.postback.data))
    booking_service = services[int(data['service_id'])]

    confirm_template_message = TemplateSendMessage(
        alt_text='請確認預約項目',
        template=ConfirmTemplate(
            text=f'您即將預約\n\n{booking_service["title"]} {booking_service["duration"]}\n預約時段: {data["date"]} {data["time"]}\n\n確認沒問題請按【確定】',
            actions=[
                PostbackAction(
                    label='確定',
                    display_text='確定沒問題！',
                    data=f'action=confirmed&service_id={data["service_id"]}&date={data["date"]}&time={data["time"]}'
                ),
                MessageAction(
                    label='重新預約',
                    text='我想重新預約'
                )
            ]
        )
    )
    line_bot_api.reply_message(
        event.reply_token,
        [confirm_template_message])


def is_booked(event, user):
    reservation = Reservation.query.filter(Reservation.user_id == user.id,
                                           Reservation.is_canceled.is_(False),#代表沒有被取消
                                           Reservation.booking_datetime > datetime.datetime.now()).first()
                                           #需要大於當下的時間.first()是會回傳第一筆資料
    if reservation:#text顯示預約項目名稱和服務時段
        buttons_template_message = TemplateSendMessage(
            alt_text='您已經有預約了，是否需要取消?',
            template=ButtonsTemplate(
                title='您已經有預約了',
                text=f'{reservation.booking_service}\n預約時段: {reservation.booking_datetime}',
                actions=[
                    PostbackAction(
                        label='我想取消預約',
                        display_text='我想取消預約',
                        data='action=cancel'
                    )
                ]
            )
        )

        line_bot_api.reply_message(
            event.reply_token,
            [buttons_template_message])

        return True
    else:
        return False
    

def service_confirmed_event(event):
    data = dict(parse_qsl(event.postback.data))

    booking_service = services[int(data['service_id'])]
    booking_datetime = datetime.datetime.strptime(f'{data["date"]} {data["time"]}', '%Y-%m-%d %H:%M')

    user = User.query.filter(User.line_id == event.source.user_id).first()
    if is_booked(event, user):
        return
    
    reservation = Reservation(
        user_id=user.id,
        booking_service_category=f'{booking_service["category"]}',
        booking_service=f'{booking_service["title"]} {booking_service["duration"]}',
        booking_datetime=booking_datetime)

    db.session.add(reservation)
    db.session.commit()

    line_bot_api.reply_message(
        event.reply_token,
        [TextSendMessage(text='沒問題！感謝您的預約，我已經幫你預約成功了喔，到時候見！')])
    
def service_cancel_event(event):

    user = User.query.filter(User.line_id == event.source.user_id).first()
    reservation = Reservation.query.filter(Reservation.user_id == user.id,
                                           Reservation.is_canceled.is_(False),
                                           Reservation.booking_datetime > datetime.datetime.now()).first()
    
    if reservation:
        reservation.is_canceled = True

        db.session.add(reservation)
        db.session.commit()

        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text='您的預約已經幫你取消了')]
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text='您目前沒有預約哦')]
        )

def text_event(event):
    flex_message = FlexSendMessage(
        alt_text='hello',
        contents={
            'type': 'bubble'
        }
    )