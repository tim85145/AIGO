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

    text_message = TextSendMessage(text = """$ Master SPA $
專業中醫推拿出身，融合東西方按摩手法
                                   
-嚴格把關：所有用品皆有消毒或採一次用品。
                                   
-設備齊全：夏天有冷氣，冬天有電毯和暖氣。
                                   
-獨立空間：專業乾淨高品質獨立按摩空間。""", emojis=emoji)
    
    sticker_message = StickerSendMessage(
        package_id = '8522',
        sticker_id = '16581271'
    )

    about_us_img = "https://i.imgur.com/70A4WdI.jpg"

    image_message = ImageSendMessage(
        original_content_url = about_us_img,
        preview_image_url = about_us_img
    )

    line_bot_api.reply_message(
        event.reply_token,
        [text_message, sticker_message, image_message]
    )

def location_event(event):
    location_message = LocationSendMessage(
        title = 'Master SPA',
        address = '聯成電腦',
        latitude = 22.63506,
        longitude = 120.30201
    )

    line_bot_api.reply_message(
        event.reply_token,
        location_message
    )