from abc import ABC, abstractmethod
from bot.handlers.handler_status import HandlerStatus

class Handler(ABC):
    @abstractmethod
    def can_handle(self, update: dict, state: str, data:dict) -> bool : ...
    
    @abstractmethod

    def handle(self, update: dict, state: str, data:dict) -> HandlerStatus : ...
    