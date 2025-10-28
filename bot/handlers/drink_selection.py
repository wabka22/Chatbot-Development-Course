from bot.domain.messenger import Messenger
from bot.domain.storage import Storage
from bot.handlers.handler import Handler, HandlerStatus
from bot.bot_core.keyboards import Keyboards


class DrinkSelection(Handler):
    def can_handle(
        self,
        update: dict,
        state: str,
        data: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> bool:
        if "callback_query" not in update:
            return False

        if state != "WAIT_FOR_DRINKS":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("drink_")

    def handle(
        self,
        update: dict,
        state: str,
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

        data["drink"] = selected_drink

        storage.update_user_data(telegram_id, data)
        storage.update_user_state(telegram_id, "WAIT_FOR_ORDER_APPROVE")
        messenger.answer_callback_query(update["callback_query"]["id"])

        messenger.deleteMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"],
        )

        pizza_name = data.get("pizza_name", "Неизвестно")
        pizza_size = data.get("pizza_size", "Неизвестно")
        drink = data.get("drink", "Неизвестно")

        order_summary = f"""🍕 **Ваш заказ:**

**Пицца:** {pizza_name}
**Размер:** {pizza_size}
**Напиток:** {drink}

Всё верно?"""

        messenger.sendMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            text=order_summary,
            parse_mode="Markdown",
            reply_markup=Keyboards.order_confirmation(),
        )
        return HandlerStatus.STOP
