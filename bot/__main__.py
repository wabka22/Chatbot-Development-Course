from bot.bot_core.long_polling import long_polling
from bot.bot_core.dispatcher import Dispatcher
from bot.domain.messenger import Messenger
from bot.domain.storage import Storage
from bot.handlers import get_handlers
from bot.infrastructure.sqlite import SqliteStorage
from bot.infrastructure.telegram import MessengerTelegram


def main() -> None:
    try:
        storage: Storage = SqliteStorage()
        messenger: Messenger = MessengerTelegram()

        dispatcher = Dispatcher(storage, messenger)
        dispatcher.add_handlers(*get_handlers())
        long_polling(dispatcher, messenger)
    except KeyboardInterrupt:
        print("\nBye!")


if __name__ == "__main__":
    main()
