from bot.handler import Handler
import bot.telegram_client

class VoiceEcho(Handler):
    def can_handle(self, update: dict) -> bool:
        return "message" in update and "voice" in update["message"]
    
    def handle(self, update: dict) -> bool:
        voice_file_id = update["message"]["voice"]["file_id"]
        
        bot.telegram_client.sendVoice(
            chat_id=update["message"]["chat"]["id"],
            voice=voice_file_id
        )
        return True