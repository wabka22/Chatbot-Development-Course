from bot.bot_core.dispatcher import Dispatcher
from bot.handlers.pizza_selection import PizzaSelection
from bot.domain.order_state import OrderState
from tests.mocks import Mock
import json
import pytest


@pytest.mark.asyncio
async def test_pizza_selection_handler():
    test_update = {
        "update_id": 123456789,
        "callback_query": {
            "id": "test_callback_id",
            "from": {"id": 12345, "is_bot": False, "first_name": "Test"},
            "message": {"message_id": 100, "chat": {"id": 12345}},
            "data": "pizza_margherita",
        },
    }

    update_user_data_called = False
    get_user_called = False

    async def update_user_data(telegram_id: int, **kwargs) -> None:
        assert telegram_id == 12345
        assert kwargs["state"] == OrderState.WAIT_FOR_PIZZA_SIZE
        order_json = kwargs["order_json"]
        assert order_json["pizza_name"] == "Margherita"
        nonlocal update_user_data_called
        update_user_data_called = True

    async def get_user(telegram_id: int) -> dict | None:
        assert telegram_id == 12345
        nonlocal get_user_called
        get_user_called = True
        return {
            "telegram_id": 12345,
            "state": OrderState.WAIT_FOR_PIZZA_NAME,
            "order_json": json.dumps({}),
        }

    answer_callback_query_called = False
    delete_message_calls = []
    send_message_calls = []

    async def answer_callback_query(callback_query_id: str, **kwargs) -> dict:
        assert callback_query_id == "test_callback_id"
        nonlocal answer_callback_query_called
        answer_callback_query_called = True
        return {"ok": True}

    async def deleteMessage(chat_id: int, message_id: int) -> dict:
        assert chat_id == 12345
        delete_message_calls.append(message_id)
        return {"ok": True}

    async def sendMessage(chat_id: int, text: str, **kwargs) -> dict:
        assert chat_id == 12345
        send_message_calls.append({"text": text, "kwargs": kwargs})
        return {"ok": True}

    mock_storage = Mock(
        {
            "update_user_data": update_user_data,
            "get_user": get_user,
        }
    )

    mock_messenger = Mock(
        {
            "answer_callback_query": answer_callback_query,
            "deleteMessage": deleteMessage,
            "sendMessage": sendMessage,
        }
    )

    dispatcher = Dispatcher(mock_storage, mock_messenger)
    dispatcher.add_handlers(PizzaSelection())
    await dispatcher.dispatch(test_update)

    assert update_user_data_called
    assert get_user_called
    assert answer_callback_query_called
    assert len(delete_message_calls) == 2
    assert 100 in delete_message_calls
    assert 99 in delete_message_calls
    assert len(send_message_calls) == 1
    assert send_message_calls[0]["text"] == "👨‍🍳 Выберите размер пиццы:"
