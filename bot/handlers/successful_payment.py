import json
from bot.domain.messenger import Messenger
from bot.domain.order_state import OrderState
from bot.domain.storage import Storage
from bot.handlers.handler import Handler, HandlerStatus


class SuccessfulPaymentHandler(Handler):
    def can_handle(
        self,
        update: dict,
        state: OrderState,
        order_json: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> bool:
        if "message" not in update:
            return False
        return "successful_payment" in update["message"]

    def handle(
        self,
        update: dict,
        state: OrderState,
        order_json: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> HandlerStatus:
        telegram_id = update["message"]["from"]["id"]
        chat_id = update["message"]["chat"]["id"]

        storage.update_user_state(telegram_id, OrderState.ORDER_FINISHED)

        user = storage.get_user(telegram_id)

        order_data = {}
        if user and user.get("order_json"):
            try:
                order_data = json.loads(user["order_json"])
            except json.JSONDecodeError:
                order_data = {}

        pizza_name = order_data.get("pizza_name", "Unknown")
        pizza_size = order_data.get("pizza_size", "Unknown")
        drink = order_data.get("drink", "Unknown")

        order_confirmation = f"""✅ **Ваш заказ принят!**
🍕 **Состав заказа:**
• Пицца: {pizza_name}
• Размер: {pizza_size}
• Напиток: {drink}

💳 Оплата успешно прошла — спасибо, что выбрали нас!  
🔥 Ваш заказ уже готовится и скоро будет доставлен.

Чтобы оформить новый заказ, отправьте команду **/start**."""

        messenger.sendMessage(
            chat_id=chat_id,
            text=order_confirmation,
            parse_mode="Markdown",
        )

        return HandlerStatus.STOP
