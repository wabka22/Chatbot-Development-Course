from bot.handlers.handler import Handler, HandlerStatus
from database.database_client import persist_update


class DatabaseLogger(Handler):
    def can_handle(self, update: dict, user_state=None, user_data=None) -> bool:
        return True

    def handle(self, update: dict, user_state=None, user_data=None) -> HandlerStatus:
        persist_update(update)
        return HandlerStatus.CONTINUE
