import json

import bot.telegram_client
import database.database_client
from bot.handlers.handler import Handler, HandlerStatus

class PizzaSelection(Handler):
    def can_handle(self, update: dict, state: str, data: dict) -> bool:
        if "callback_query" not in update:
            return False

        if state != "WAIT_FOR_PIZZA_NAME":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("pizza_")

    def handle(self, update: dict, state: str, data: dict) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        pizza_name = callback_data.replace("pizza_", "").replace("_", " ").title()
        database.database_client.update_user_data(telegram_id, {"pizza_name": pizza_name})
        database.database_client.update_user_state(telegram_id, "WAIT_FOR_PIZZA_SIZE")
        bot.telegram_client.answer_callback_query(update["callback_query"]["id"])
        
        chat_id = update["callback_query"]["message"]["chat"]["id"]
        bot.telegram_client.deleteMessage(
            chat_id=chat_id,
            message_id=update["callback_query"]["message"]["message_id"],
        )

        bot.telegram_client.deleteMessage(
            chat_id=chat_id,
            message_id=update["callback_query"]["message"]["message_id"] - 1,
        )
        
        bot.telegram_client.sendMessage(
            chat_id=chat_id,
            text="👨‍🍳 Выберите размер пиццы:",
            reply_markup=json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {"text": "👶 Small (25cm)", "callback_data": "size_small"},
                            {"text": "👦 Medium (30cm)", "callback_data": "size_medium"},
                        ],
                        [
                            {"text": "👨 Large (35cm)", "callback_data": "size_large"},
                            {"text": "🎪 XL (40cm)", "callback_data": "size_xl"},
                        ],
                    ],
                }
            ),
        )
        return HandlerStatus.STOP