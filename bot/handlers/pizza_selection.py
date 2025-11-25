import asyncio
from bot.domain.messenger import Messenger
from bot.domain.storage import Storage
from bot.handlers.handler import Handler, HandlerStatus
from bot.bot_core.keyboards import Keyboards
from bot.domain.order_state import OrderState
import json


class PizzaSelection(Handler):
    def can_handle(
        self,
        update: dict,
        state: OrderState,
        data: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> bool:
        if "callback_query" not in update:
            return False
        if state != OrderState.WAIT_FOR_PIZZA_NAME:
            return False
        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("pizza_")

    async def handle(
        self,
        update: dict,
        state: OrderState,
        data: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        pizza_name = callback_data.replace("pizza_", "").replace("_", " ").title()

        user = await storage.get_user(telegram_id)
        order_json = json.loads(user["order_json"]) if user["order_json"] else {}
        order_json["pizza_name"] = pizza_name

        await storage.update_user_data(
            telegram_id,
            state=OrderState.WAIT_FOR_PIZZA_SIZE,
            order_json=order_json,
        )

        chat_id = update["callback_query"]["message"]["chat"]["id"]

        await asyncio.gather(
            messenger.answer_callback_query(update["callback_query"]["id"]),
            messenger.deleteMessage(
                chat_id=chat_id,
                message_id=update["callback_query"]["message"]["message_id"],
            ),
            messenger.deleteMessage(
                chat_id=chat_id,
                message_id=update["callback_query"]["message"]["message_id"] - 1,
            ),
            messenger.sendMessage(
                chat_id=chat_id,
                text="👨‍🍳 Выберите размер пиццы:",
                reply_markup=Keyboards.size_selection(),
            ),
        )

        return HandlerStatus.STOP
