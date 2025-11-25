import asyncio
from bot.domain.messenger import Messenger
from bot.domain.storage import Storage
from bot.handlers.handler import Handler, HandlerStatus
from bot.bot_core.keyboards import Keyboards
from bot.domain.order_state import OrderState


class MessageStart(Handler):
    def can_handle(
        self,
        update: dict,
        state: OrderState,
        data: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> bool:
        return (
            "message" in update
            and "text" in update["message"]
            and update["message"]["text"] == "/start"
        )

    async def handle(
        self,
        update: dict,
        state: OrderState,
        data: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> HandlerStatus:
        telegram_id = update["message"]["from"]["id"]

        await storage.clear_user_data(telegram_id)
        await storage.update_user_state(telegram_id, OrderState.WAIT_FOR_PIZZA_NAME)

        await asyncio.gather(
            messenger.sendMessage(
                chat_id=update["message"]["chat"]["id"],
                text="🍕 ПРИВЕТСТВУЕМ В ЛУЧШЕЙ ПИЦЦЕРИИ! 🍕",
                reply_markup=Keyboards.remove_keyboard(),
            ),
            messenger.sendMessage(
                chat_id=update["message"]["chat"]["id"],
                text="Пожалуйста, выберите тип пиццы:",
                reply_markup=Keyboards.pizza_selection(),
            ),
        )

        return HandlerStatus.STOP
