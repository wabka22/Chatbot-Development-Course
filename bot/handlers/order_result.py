import json

import bot.telegram_client
from database.database_client import clear_user_data, update_user_state
from bot.handlers.handler import Handler, HandlerStatus

class OrderResult(Handler):
    def can_handle(self, update: dict, state: str, data: dict) -> bool:
        if "callback_query" not in update:
            return False

        if state != "WAIT_FOR_ORDER_APPROVE":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data in ["order_approve", "order_restart"]

    def handle(self, update: dict, state: str, data: dict) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        bot.telegram_client.answer_callback_query(update["callback_query"]["id"])
        bot.telegram_client.deleteMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"],
        )

        if callback_data == "order_approve":
            update_user_state(telegram_id, "ORDER_FINISHED")

            pizza_name = data.get("pizza_name", "Неизвестно")
            pizza_size = data.get("pizza_size", "Неизвестно")
            drink = data.get("drink", "Неизвестно")

            order_confirmation = f"""✅ **Заказ подтвержден!**
            🍕 **Ваш заказ:**
            • Пицца: {pizza_name}
            • Размер: {pizza_size}
            • Напиток: {drink}

            Спасибо за заказ! Ваша пицца будет готова в ближайшее время.

            Отправьте /start для нового заказа."""

            bot.telegram_client.sendMessage(
                chat_id=update["callback_query"]["message"]["chat"]["id"],
                text=order_confirmation,
                parse_mode="Markdown",
            )

        elif callback_data == "order_restart":
            clear_user_data(telegram_id)

            update_user_state(telegram_id, "WAIT_FOR_PIZZA_NAME")

            bot.telegram_client.sendMessage(
                    chat_id=update["callback_query"]["message"]["chat"]["id"],
                    text="Оформляем новый заказ 🍕 😊",
                    reply_markup=json.dumps({"remove_keyboard": True}),
                )


            bot.telegram_client.sendMessage(
                chat_id=update["callback_query"]["message"]["chat"]["id"],
                text="Пожалуйста, выберите тип пиццы:",
                reply_markup=json.dumps(
                    {
                        "inline_keyboard": [
                            [
                                {"text": "🔴 Маргарита", "callback_data": "pizza_margherita"},
                                {"text": "🌶️ Пепперони", "callback_data": "pizza_pepperoni"},
                            ],
                            [
                                {"text": "🧀🧀🧀🧀 4 Сыра", "callback_data": "pizza_quattro_formaggi"},
                                {"text": "🥓 Карбонара", "callback_data": "pizza_carbonara"},
                            ],
                            [
                                {"text": "🔥 Диабло", "callback_data": "pizza_diavola"},
                                {"text": "🥬 Веганская", "callback_data": "pizza_vegana"},
                            ],
                            [
                                {"text": "🍄 Грибная", "callback_data": "pizza_funghi"},
                                {"text": "🦐 С морепродуктами", "callback_data": "pizza_marinara"},
                            ],
                        ],
                    }
                ),
            )

        return HandlerStatus.STOP
    