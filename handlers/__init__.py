from bot.handlers.handler import Handler
from bot.handlers.database_logger import DatabaseLogger
from bot.handlers.ensure_user_exists import EnsureUserExists
from bot.handlers.start_message import MessageStart
from bot.handlers.pizza_selection import PizzaSelection

def get_handlers() -> list[Handler] :
    return [
        DatabaseLogger(),
        EnsureUserExists(),
        MessageStart(),
        PizzaSelection()
    ]