from bot.handlers.handler import Handler
from bot.handlers.database_logger import DatabaseLogger
from bot.handlers.ensure_user_exists import EnsureUserExists
from bot.handlers.start_message import MessageStart
from bot.handlers.pizza_selection import PizzaSelection
from bot.handlers.size_selection import SizeSelection
from bot.handlers.drink_selection import DrinkSelection
from bot.handlers.order_result import OrderResult

HANDLERS_CONFIG = [
    DatabaseLogger,
    EnsureUserExists,
    MessageStart,
    PizzaSelection,
    SizeSelection,
    DrinkSelection,
    OrderResult,
]


def get_handlers() -> list[Handler]:
    return [handler_class() for handler_class in HANDLERS_CONFIG]
