from bot.domain.messenger import Messenger
from bot.domain.storage import Storage
from bot.handlers.handler import Handler, HandlerStatus
from bot.bot_core.keyboards import Keyboards
from bot.domain.order_state import OrderState


class OrderApprovalRestartHandler(Handler):
    def can_handle(
        self,
        update: dict,
        state: OrderState,
        order_json: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> bool:
        return (
            "callback_query" in update
            and state == OrderState.WAIT_FOR_ORDER_APPROVE
            and update["callback_query"]["data"] == "order_restart"
        )

    def handle(
        self,
        update: dict,
        state: OrderState,
        order_json: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        chat_id = update["callback_query"]["message"]["chat"]["id"]

        messenger.answer_callback_query(update["callback_query"]["id"])

        storage.clear_user_order_json(telegram_id)
        storage.update_user_data(
            telegram_id,
            state=OrderState.WAIT_FOR_PIZZA_NAME,
            order_json={},  # Пустой заказ
        )

        messenger.sendMessage(
            chat_id=chat_id,
            text="🍕 Выберите пиццу:",
            reply_markup=Keyboards.pizza_selection(),
        )

        return HandlerStatus.STOP
