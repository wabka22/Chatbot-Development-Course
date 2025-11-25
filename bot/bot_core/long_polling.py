from bot.domain.messenger import Messenger
from bot.bot_core.dispatcher import Dispatcher


async def start_long_polling(dispatcher: Dispatcher, messenger: Messenger) -> None:
    next_update_offset = 0
    while True:
        updates = await messenger.getUpdates(offset=next_update_offset, timeout=30)
        for update in updates:
            next_update_offset = max(next_update_offset, update["update_id"] + 1)
            await dispatcher.dispatch(update)
