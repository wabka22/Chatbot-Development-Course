from bot.domain.messenger import Messenger
from bot.domain.storage import Storage
from bot.handlers.handler import Handler, HandlerStatus
from bot.bot_core.keyboards import Keyboards
from bot.domain.order_state import OrderState


class PizzaSelection(Handler):
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

        if state != OrderState.WAIT_FOR_PIZZA_NAME:
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("pizza_")

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

        pizza_name = callback_data.replace("pizza_", "").replace("_", " ").title()

        data["pizza_name"] = pizza_name
        storage.update_user_data(telegram_id, data)
        storage.update_user_state(telegram_id, OrderState.WAIT_FOR_PIZZA_SIZE)
        messenger.answer_callback_query(update["callback_query"]["id"])

        chat_id = update["callback_query"]["message"]["chat"]["id"]

        messenger.deleteMessage(
            chat_id=chat_id,
            message_id=update["callback_query"]["message"]["message_id"],
        )

        messenger.deleteMessage(
            chat_id=chat_id,
            message_id=update["callback_query"]["message"]["message_id"] - 1,
        )

        messenger.sendMessage(
            chat_id=chat_id,
            text="👨‍🍳 Выберите размер пиццы:",
            reply_markup=Keyboards.size_selection(),
        )
        return HandlerStatus.STOP
