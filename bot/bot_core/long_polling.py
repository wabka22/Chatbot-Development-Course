import time
from bot.domain.messenger import Messenger
from bot.bot_core.dispatcher import Dispatcher


def long_polling(dispatcher: Dispatcher, messenger: Messenger) -> None:
    next_update_offset = 0
    while True:
        updates = messenger.getUpdates(offset=next_update_offset)
        for update in updates:
            next_update_offset = max(next_update_offset, update["update_id"] + 1)
            dispatcher.dispatch(update)
            print(".", end="", flush=True)
        time.sleep(1)
