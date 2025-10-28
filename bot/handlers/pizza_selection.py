from bot.domain.messenger import Messenger
from bot.domain.storage import Storage
from bot.handlers.handler import Handler, HandlerStatus
from bot.bot_core.keyboards import Keyboards


class PizzaSelection(Handler):
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

        if state != "WAIT_FOR_PIZZA_NAME":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("pizza_")

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

        pizza_name = callback_data.replace("pizza_", "").replace("_", " ").title()
        storage.database_client.update_user_data(
            telegram_id, {"pizza_name": pizza_name}
        )
        storage.database_client.update_user_state(telegram_id, "WAIT_FOR_PIZZA_SIZE")
        messenger.telegram_client.answer_callback_query(update["callback_query"]["id"])

        chat_id = update["callback_query"]["message"]["chat"]["id"]

        messenger.telegram_client.deleteMessage(
            chat_id=chat_id,
            message_id=update["callback_query"]["message"]["message_id"],
        )

        messenger.telegram_client.deleteMessage(
            chat_id=chat_id,
            message_id=update["callback_query"]["message"]["message_id"] - 1,
        )

        messenger.telegram_client.sendMessage(
            chat_id=chat_id,
            text="👨‍🍳 Выберите размер пиццы:",
            reply_markup=Keyboards.size_selection(),
        )
        return HandlerStatus.STOP
