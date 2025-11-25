from bot.domain.messenger import Messenger
from bot.domain.storage import Storage
from bot.handlers.handler import Handler, HandlerStatus
from bot.domain.order_state import OrderState


class DatabaseLogger(Handler):
    def can_handle(
        self,
        update: dict,
        state: OrderState,
        data: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> bool:
        return True

    async def handle(
        self,
        update: dict,
        state: OrderState,
        data: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> HandlerStatus:
        await storage.persist_update(update)
        return HandlerStatus.CONTINUE
