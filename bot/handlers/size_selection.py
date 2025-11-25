import asyncio
from bot.domain.messenger import Messenger
from bot.domain.storage import Storage
from bot.handlers.handler import Handler, HandlerStatus
from bot.bot_core.keyboards import Keyboards
from bot.domain.order_state import OrderState
import json


class SizeSelection(Handler):
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
        if state != OrderState.WAIT_FOR_PIZZA_SIZE:
            return False
        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("size_")

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

        size_mapping = {
            "size_small": "Маленькая (25cm)",
            "size_medium": "Средняя (30cm)",
            "size_large": "Большая (35cm)",
            "size_xl": "Огромная (40cm)",
        }
        pizza_size = size_mapping.get(callback_data)

        user = await storage.get_user(telegram_id)
        order_json = json.loads(user["order_json"]) if user["order_json"] else {}
        order_json["pizza_size"] = pizza_size

        chat_id = update["callback_query"]["message"]["chat"]["id"]

        await asyncio.gather(
            storage.update_user_data(
                telegram_id,
                state=OrderState.WAIT_FOR_DRINKS,
                order_json=order_json,
            ),
            messenger.answer_callback_query(update["callback_query"]["id"]),
            messenger.deleteMessage(
                chat_id=chat_id,
                message_id=update["callback_query"]["message"]["message_id"],
            ),
            messenger.sendMessage(
                chat_id=chat_id,
                text="🍻 Выберите напиток к пицце:",
                reply_markup=Keyboards.drinks_selection(),
            ),
        )

        return HandlerStatus.STOP
