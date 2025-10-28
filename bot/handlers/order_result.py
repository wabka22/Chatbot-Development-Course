from bot.domain.messenger import Messenger
from bot.domain.storage import Storage
from bot.handlers.handler import Handler, HandlerStatus
from bot.bot_core.keyboards import Keyboards


class OrderResult(Handler):
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

        if state != "WAIT_FOR_ORDER_APPROVE":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data in ["order_approve", "order_restart"]

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

        messenger.telegram_client.answer_callback_query(update["callback_query"]["id"])
        messenger.telegram_client.deleteMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"],
        )

        if callback_data == "order_approve":
            storage.update_user_state(telegram_id, "ORDER_FINISHED")

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

            messenger.telegram_client.sendMessage(
                chat_id=update["callback_query"]["message"]["chat"]["id"],
                text=order_confirmation,
                parse_mode="Markdown",
            )

        elif callback_data == "order_restart":
            storage.clear_user_data(telegram_id)
            storage.update_user_state(telegram_id, "WAIT_FOR_PIZZA_NAME")

            messenger.telegram_client.sendMessage(
                chat_id=update["callback_query"]["message"]["chat"]["id"],
                text="Оформляем новый заказ 🍕 😊",
                reply_markup=Keyboards.remove_keyboard(),
            )

            messenger.telegram_client.sendMessage(
                chat_id=update["callback_query"]["message"]["chat"]["id"],
                text="Пожалуйста, выберите тип пиццы:",
                reply_markup=Keyboards.pizza_selection(),
            )

        return HandlerStatus.STOP
