from bot.handlers.database_logger import DatabaseLogger
from bot.long_polling import start_long_polling

def get_handlers() -> list[Handler] :
    return [
        DatabaseLogger(),
        ...
    ]