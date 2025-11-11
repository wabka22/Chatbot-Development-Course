from abc import ABC, abstractmethod
from bot.domain.order_state import OrderState


class Storage(ABC):
    @abstractmethod
    def ensure_user_exists(self, telegram_id: int) -> None: ...

    @abstractmethod
    def get_user(self, telegram_id: int) -> dict: ...

    @abstractmethod
    def update_user_state(self, telegram_id: int, state: OrderState) -> None: ...

    @abstractmethod
    def update_user_data(self, telegram_id: int, data: dict) -> None: ...

    @abstractmethod
    def clear_user_data(self, telegram_id: int) -> None: ...

    @abstractmethod
    def persist_update(self, update: dict) -> None: ...
