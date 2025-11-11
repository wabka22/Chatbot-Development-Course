from bot.handlers.handler import Handler
from bot.handlers.database_logger import DatabaseLogger
from bot.handlers.ensure_user_exists import EnsureUserExists
from bot.handlers.start_message import MessageStart
from bot.handlers.pizza_selection import PizzaSelection
from bot.handlers.size_selection import SizeSelection
from bot.handlers.drink_selection import DrinkSelection
from bot.handlers.pre_checkout_query import PreCheckoutQueryHandler
from bot.handlers.successful_payment import SuccessfulPaymentHandler
from bot.handlers.order_approved import OrderApprovalApprovedHandler
from bot.handlers.order_restart import OrderApprovalRestartHandler


def get_handlers() -> list[Handler]:
    return [
        DatabaseLogger(),
        EnsureUserExists(),
        MessageStart(),
        PizzaSelection(),
        SizeSelection(),
        DrinkSelection(),
        OrderApprovalApprovedHandler(),
        OrderApprovalRestartHandler(),
        PreCheckoutQueryHandler(),
        SuccessfulPaymentHandler(),
    ]
