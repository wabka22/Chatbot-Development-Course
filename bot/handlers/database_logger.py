from bot.handlers.handler import Handler
from bot.database_client import persist_update

class DatabaseLogger(Handler):
    def can_handle(self, update: dict) -> bool:
        return True
    
    def handle(self, update: dict) -> bool:
        persist_update(update)
        return Handler.CONTINUE
    