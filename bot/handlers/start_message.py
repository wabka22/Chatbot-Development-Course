from bot.domain.messenger import Messenger
from bot.domain.storage import Storage
from bot.handlers.handler import Handler, HandlerStatus
from bot.bot_core.keyboards import Keyboards


class MessageStart(Handler):
    def can_handle(
        self,
        update: dict,
        state: str,
        data: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> bool:
        return (
            "message" in update
            and "text" in update["message"]
            and update["message"]["text"] == "/start"
        )

    def handle(
        self,
        update: dict,
        state: str,
        data: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> HandlerStatus:
        telegram_id = update["message"]["from"]["id"]

        storage.database_client.clear_user_data(telegram_id)
        storage.database_client.update_user_state(telegram_id, "WAIT_FOR_PIZZA_NAME")

        messenger.telegram_client.sendMessage(
            chat_id=update["message"]["chat"]["id"],
            text="🍕 ПРИВЕТСТВУЕМ В ЛУЧШЕЙ ПИЦЦЕРИИ! 🍕",
            reply_markup=Keyboards.remove_keyboard(),
        )

        messenger.telegram_client.sendMessage(
            chat_id=update["message"]["chat"]["id"],
            text="Пожалуйста, выберите тип пиццы:",
            reply_markup=Keyboards.pizza_selection(),
        )

        return HandlerStatus.STOP
