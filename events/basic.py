from line_bot_api import *

def about_us_event(event):
    emoji = [
        {
            "index": 0,
            "productId": "5ac21e6c040ab15980c9b444",
            "emojiId": "010"
        },
        {
            "index": 13,
            "productId": "5ac1bfd5040ab15980c9b435",
            "emojiId": "021"
        }
    ]

    # 文字訊息
    text_message = TextSendMessage(text = """$ Master SPA $
專業中醫推拿出身，融合東西方按摩手法
                                   
-嚴格把關：所有用品皆有消毒或採一次用品。
                                   
-設備齊全：夏天有冷氣，冬天有電毯和暖氣。
                                   
-獨立空間：專業乾淨高品質獨立按摩空間。""", emojis=emoji)
    
    # 貼圖訊息
    sticker_message = StickerSendMessage(
        package_id = '8522',
        sticker_id = '16581271'
    )
    
    about_us_img = "https://i.imgur.com/DdzReRy.png"

    # 圖片訊息
    image_message = ImageSendMessage(
        original_content_url = about_us_img,
        preview_image_url = about_us_img
    )

    # 把上面的訊息丟進回復訊息內
    line_bot_api.reply_message(
        event.reply_token,
        [text_message, sticker_message, image_message]
    )

def location_event(event):
    location_message = LocationSendMessage(
        title = 'J髮時尚',
        address = '820高雄市岡山區介壽西路153號內部',
        latitude = 22.784337712398127,        # 22.784337712398127, 120.28094068650512
        longitude = 120.28094068650512
    )

    line_bot_api.reply_message(
        event.reply_token,
        location_message
    )