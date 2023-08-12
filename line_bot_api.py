from linebot import LineBotApi, WebhookHandler  #連接Line Bot的兩個函數
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, FollowEvent, UnfollowEvent, 
                            StickerSendMessage, ImageSendMessage, LocationSendMessage, FlexSendMessage,
                            TemplateSendMessage, ImageCarouselTemplate, ImageCarouselColumn, PostbackAction,
                            PostbackEvent)

handler = WebhookHandler('e0a330649a4718082f73cad08fc9c8aa')  #Basic Setting -> Channel Secret
line_bot_api = LineBotApi('srkXgtopvnAYhHLBQpq3lU54N7pNim8v79fql1WQPw8iwLBPfwPYrH1CKYageRyQyauWq0kF8kjcT2EQHV3QK0qFJSAuFkjcRjPfMmltgtPe6qQnVfafMnRjtz7Tb0NWYDC68mzTpuDAJmiJRo1aXwdB04t89/1O/w1cDnyilFU=')   #Messaging API -> Channel access token
