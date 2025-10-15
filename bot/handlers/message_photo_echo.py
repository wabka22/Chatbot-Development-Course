from bot.handler import Handler
import bot.telegram_client

class MessagePhotoEcho(Handler):
    def can_handle(self, update: dict) -> bool:
        return "message" in update and "photo" in update["message"]
    
    def handle(self, update: dict) -> bool:
        photos = update["message"]["photo"]
        max_size_photo = max(photos, key=lambda photo: photo["file_size"])
        file_id = max_size_photo["file_id"]
        
        bot.telegram_client.sendPhoto(
            chat_id=update["message"]["chat"]["id"],
            photo=file_id
        )
        return True