from bot.bot_core.dispatcher import Dispatcher
from bot.handlers.start_message import MessageStart
from bot.domain.order_state import OrderState
from tests.mocks import Mock


def test_message_start_handler():
    test_update = {
        "update_id": 123456789,
        "message": {
            "message_id": 1,
            "from": {
                "id": 12345,
                "is_bot": False,
                "first_name": "Test",
                "username": "test_user",
            },
            "chat": {
                "id": 12345,
                "first_name": "Test",
                "username": "test_user",
                "type": "private",
            },
            "date": 1640995200,
            "text": "/start",
        },
    }

    clear_user_data_called = False
    update_user_state_called = False

    def clear_user_data(telegram_id: int) -> None:
        assert telegram_id == 12345
        nonlocal clear_user_data_called
        clear_user_data_called = True

    def update_user_state(telegram_id: int, state: OrderState) -> None:
        assert telegram_id == 12345
        assert state == OrderState.WAIT_FOR_PIZZA_NAME
        nonlocal update_user_state_called
        update_user_state_called = True

    def get_user(telegram_id: int) -> dict | None:
        assert telegram_id == 12345
        return {"state": None, "order_json": "{}"}

    sendMessage_calls = []

    def sendMessage(chat_id: int, text: str, **kwargs) -> dict:
        assert chat_id == 12345
        sendMessage_calls.append({"text": text})
        return {"ok": True}

    mock_storage = Mock(
        {
            "clear_user_data": clear_user_data,
            "update_user_state": update_user_state,
            "get_user": get_user,
        }
    )
    mock_messenger = Mock({"sendMessage": sendMessage})

    dispatcher = Dispatcher(mock_storage, mock_messenger)
    dispatcher.add_handlers(MessageStart())
    dispatcher.dispatch(test_update)

    assert clear_user_data_called
    assert update_user_state_called
    assert len(sendMessage_calls) == 2
    assert "ПИЦЦЕРИИ" in sendMessage_calls[0]["text"]
    assert "выберите тип пиццы" in sendMessage_calls[1]["text"]
