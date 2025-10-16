from bot.handler import Handler
import bot.telegram_client

class DocumentEcho(Handler):
    def can_handle(self, update: dict) -> bool:
        return "message" in update and "document" in update["message"]
    
    def handle(self, update: dict) -> bool:
        document_file_id = update["message"]["document"]["file_id"]
        file_name = update["message"]["document"].get("file_name", "document")
        
        bot.telegram_client.sendDocument(
            chat_id=update["message"]["chat"]["id"],
            document=document_file_id,
            caption=f"Ваш файл: {file_name}"
        )
        return False