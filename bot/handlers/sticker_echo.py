from bot.handler import Handler
import bot.telegram_client

class StickerEcho(Handler):
    def can_handle(self, update: dict) -> bool:
        return "message" in update and "sticker" in update["message"]
    
    def handle(self, update: dict) -> bool:
        sticker_file_id = update["message"]["sticker"]["file_id"]
        
        bot.telegram_client.sendSticker(
            chat_id=update["message"]["chat"]["id"],
            sticker=sticker_file_id
        )
        return True