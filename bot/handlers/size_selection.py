import json

import bot.telegram_client
import database.database_client
from bot.handlers.handler import Handler,HandlerStatus

class SizeHandler(Handler):
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
            "size_small": "Small (25cm)",
            "size_medium": "Medium (30cm)",
            "size_large": "Large (35cm)",
            "size_xl": "Extra Large (40cm)",
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
            reply_markup=json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {"text": "🔴 Coca-Cola", "callback_data": "drink_coca_cola"},
                            {"text": "🔵 Pepsi", "callback_data": "drink_pepsi"},
                        ],
                        [
                            {"text": "🍊 Апельсиновый сок", "callback_data": "drink_orange_juice"},
                            {"text": "🍎 Яблочный сок", "callback_data": "drink_apple_juice"},
                        ],
                        [
                            {"text": "💧 Минеральная вода", "callback_data": "drink_water"},
                            {"text": "🥤 Холодный чай Lipton", "callback_data": "drink_iced_tea"},
                        ],
                        [
                            {"text": "🚫 Без напитков", "callback_data": "drink_none"},
                        ],
                    ],
                }
            ),
        )
        return HandlerStatus.STOP
    