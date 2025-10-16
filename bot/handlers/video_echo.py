from bot.handler import Handler
import bot.telegram_client

class VideoEcho(Handler):
    def can_handle(self, update: dict) -> bool:
        return "message" in update and "video" in update["message"]
    
    def handle(self, update: dict) -> bool:
        video_file_id = update["message"]["video"]["file_id"]
        
        bot.telegram_client.sendVideo(
            chat_id=update["message"]["chat"]["id"],
            video=video_file_id
        )
        return False