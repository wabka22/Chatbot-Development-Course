from bot.bot_core.long_polling import start_long_polling
from bot.bot_core.dispatcher import Dispatcher
from bot.domain.messenger import Messenger
from bot.domain.storage import Storage
from bot.handlers import get_handlers
from bot.infrastructure.postgres import StoragePostgres
from bot.infrastructure.telegram import MessengerTelegram


def main() -> None:
    try:
        storage: Storage = StoragePostgres()
        messenger: Messenger = MessengerTelegram()

        dispatcher = Dispatcher(storage, messenger)
        dispatcher.add_handlers(*get_handlers())
        start_long_polling(dispatcher, messenger)
    except KeyboardInterrupt:
        print("\nBye!")


if __name__ == "__main__":
    main()
