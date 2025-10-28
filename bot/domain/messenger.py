from abc import ABC, abstractmethod


class Messenger(ABC):
    @abstractmethod
    def sendMessage(self, chat_id: int, text: str, **kwargs) -> dict: ...

    @abstractmethod
    def getUpdates(self, **kwargs) -> dict: ...

    @abstractmethod
    def answer_callback_query(self, callback_query_id: str, **kwargs) -> dict: ...

    @abstractmethod
    def deleteMessage(self, chat_id: int, message_id: int) -> dict: ...
