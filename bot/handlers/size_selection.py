import bot.telegram_client
import database.database_client
from bot.handlers.handler import Handler, HandlerStatus
from bot.keyboards import Keyboards


class SizeSelection(Handler):
    def can_handle(self, update: dict, state: str, data: dict) -> bool:
        if "callback_query" not in update:
            return False

        if state != "WAIT_FOR_PIZZA_SIZE":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("size_")

    def handle(self, update: dict, state: str, data: dict) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        size_mapping = {
            "size_small": "Маленькая (25cm)",
            "size_medium": "Средняя (30cm)",
            "size_large": "Большая (35cm)",
            "size_xl": "Супер большая (40cm)",
        }

        pizza_size = size_mapping.get(callback_data)
        data["pizza_size"] = pizza_size
        database.database_client.update_user_data(telegram_id, data)
        database.database_client.update_user_state(telegram_id, "WAIT_FOR_DRINKS")

        bot.telegram_client.answer_callback_query(update["callback_query"]["id"])

        bot.telegram_client.deleteMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"],
        )

        bot.telegram_client.sendMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            text="🍻 Выберите напиток к пицце:",
            reply_markup=Keyboards.drinks_selection(),
        )
        return HandlerStatus.STOP
