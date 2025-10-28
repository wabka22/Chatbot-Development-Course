from bot.domain.messenger import Messenger
from bot.domain.storage import Storage
from bot.handlers.handler import Handler, HandlerStatus
from bot.bot_core.keyboards import Keyboards


class SizeSelection(Handler):
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

        if state != "WAIT_FOR_PIZZA_SIZE":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("size_")

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

        size_mapping = {
            "size_small": "Маленькая (25cm)",
            "size_medium": "Средняя (30cm)",
            "size_large": "Большая (35cm)",
            "size_xl": "Супер большая (40cm)",
        }

        pizza_size = size_mapping.get(callback_data)
        data["pizza_size"] = pizza_size
        storage.update_user_data(telegram_id, data)
        storage.update_user_state(telegram_id, "WAIT_FOR_DRINKS")

        messenger.answer_callback_query(update["callback_query"]["id"])

        messenger.deleteMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"],
        )

        messenger.sendMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            text="🍻 Выберите напиток к пицце:",
            reply_markup=Keyboards.drinks_selection(),
        )
        return HandlerStatus.STOP
