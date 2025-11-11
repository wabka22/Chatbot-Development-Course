from bot.domain.messenger import Messenger
from bot.domain.storage import Storage
from bot.handlers.handler import Handler, HandlerStatus
from bot.bot_core.keyboards import Keyboards
from bot.domain.order_state import OrderState
import json


class DrinkSelection(Handler):
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
        if state != OrderState.WAIT_FOR_DRINKS:
            return False
        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("drink_")

    def handle(
        self,
        update: dict,
        state: OrderState,
        data: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        drink_mapping = {
            "drink_coca_cola": "Coca-Cola",
            "drink_pepsi": "Pepsi",
            "drink_orange_juice": "Апельсиновый сок",
            "drink_apple_juice": "Яблочный сок",
            "drink_water": "Вода",
            "drink_iced_tea": "Холодный чай",
            "drink_none": "Без напитка",
        }
        selected_drink = drink_mapping.get(callback_data)

        user = storage.get_user(telegram_id)
        order_json = json.loads(user["order_json"]) if user["order_json"] else {}
        order_json["drink"] = selected_drink

        storage.update_user_data(
            telegram_id,
            state=OrderState.WAIT_FOR_ORDER_APPROVE,
            order_json=order_json,
        )

        messenger.answer_callback_query(update["callback_query"]["id"])
        chat_id = update["callback_query"]["message"]["chat"]["id"]

        messenger.deleteMessage(
            chat_id=chat_id,
            message_id=update["callback_query"]["message"]["message_id"],
        )

        pizza_name = order_json.get("pizza_name", "Неизвестно")
        pizza_size = order_json.get("pizza_size", "Неизвестно")
        drink = order_json.get("drink", "Неизвестно")

        order_summary = f"""🍕 **Ваш заказ:**

**Пицца:** {pizza_name}
**Размер:** {pizza_size}
**Напиток:** {drink}

Всё верно?"""

        messenger.sendMessage(
            chat_id=chat_id,
            text=order_summary,
            parse_mode="Markdown",
            reply_markup=Keyboards.order_confirmation(),
        )
        return HandlerStatus.STOP
