import asyncio
import json
import os
from dotenv import load_dotenv
from bot.domain.messenger import Messenger
from bot.domain.order_state import OrderState
from bot.domain.storage import Storage
from bot.handlers.handler import Handler, HandlerStatus

load_dotenv()


class OrderApprovalApprovedHandler(Handler):
    def can_handle(
        self,
        update: dict,
        state: OrderState,
        order_json: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> bool:
        if "callback_query" not in update:
            return False

        if state != OrderState.WAIT_FOR_ORDER_APPROVE:
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data == "order_approve"

    async def handle(
        self,
        update: dict,
        state: OrderState,
        order_json: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        chat_id = update["callback_query"]["message"]["chat"]["id"]

        user = await storage.get_user(telegram_id)
        current_order_json = (
            json.loads(user["order_json"]) if user["order_json"] else {}
        )

        pizza_name = current_order_json.get("pizza_name", "Неизвестно")
        pizza_size = current_order_json.get("pizza_size", "Неизвестно")
        drink = current_order_json.get("drink", "Неизвестно")

        await asyncio.gather(
            messenger.answer_callback_query(update["callback_query"]["id"]),
            messenger.deleteMessage(
                chat_id=chat_id,
                message_id=update["callback_query"]["message"]["message_id"],
            ),
            storage.update_user_state(telegram_id, OrderState.WAIT_FOR_PAYMENT),
        )

        pizza_prices = {
            "Маленькая (25cm)": 35000,
            "Средняя (30cm)": 55000,
            "Большая (35cm)": 65000,
            "Огромная (40cm)": 75000,
        }

        drink_price = 10000  # 100.00 RUB

        pizza_price = pizza_prices.get(pizza_size, 60000)

        prices = [
            {"label": f"Пицца {pizza_name} ({pizza_size})", "amount": pizza_price}
        ]

        if drink and drink not in ("Без напитка", "Неизвестно"):
            prices.append({"label": f"Напиток: {drink}", "amount": drink_price})

        order_payload = json.dumps(
            {
                "tid": telegram_id,
                "p": pizza_name[:10],
                "s": pizza_size[:1],
                "d": (
                    drink[:5] if drink not in ("Без напитка", "Неизвестно") else "none"
                ),
            }
        )

        provider_token = os.getenv("YOOKASSA_TOKEN")
        if not provider_token:
            raise ValueError("YOOKASSA_TOKEN environment variable is not set")

        try:
            await messenger.send_invoice(
                chat_id=update["callback_query"]["message"]["chat"]["id"],
                title="Pizza Order",
                description=f"Pizza: {pizza_name}, Size: {pizza_size}, Drink: {drink}",
                payload=order_payload,
                provider_token=os.getenv("YOOKASSA_TOKEN"),
                currency="RUB",
                prices=prices,
            )
            print(f"Invoice sent successfully to user {telegram_id}")
        except Exception as e:
            print(f"Error sending invoice: {e}")
            await messenger.sendMessage(
                chat_id=chat_id,
                text=" Произошла ошибка при создании счета. Пожалуйста, попробуйте позже.",
            )
            await storage.update_user_state(
                telegram_id, OrderState.WAIT_FOR_ORDER_APPROVE
            )

        return HandlerStatus.STOP
