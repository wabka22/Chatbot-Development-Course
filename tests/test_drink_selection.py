from bot.bot_core.dispatcher import Dispatcher
from bot.handlers.drink_selection import DrinkSelection
from tests.mocks import Mock


def test_drink_selection_handler():
    test_update = {
        "update_id": 123456789,
        "callback_query": {
            "id": "test_callback_id",
            "from": {
                "id": 12345,
                "is_bot": False,
                "first_name": "Test",
            },
            "message": {
                "message_id": 100,
                "chat": {"id": 12345},
            },
            "data": "drink_coca_cola",
        },
    }

    update_user_data_called = False
    update_user_state_called = False

    def update_user_data(telegram_id: int, data: dict) -> None:
        assert telegram_id == 12345
        assert data["drink"] == "Coca-Cola"
        nonlocal update_user_data_called
        update_user_data_called = True

    def update_user_state(telegram_id: int, state: str) -> None:
        assert telegram_id == 12345
        assert state == "WAIT_FOR_ORDER_APPROVE"
        nonlocal update_user_state_called
        update_user_state_called = True

    def get_user(telegram_id: int) -> dict | None:
        assert telegram_id == 12345
        return {
            "state": "WAIT_FOR_DRINKS",
            "data": {"pizza_name": "Margherita", "pizza_size": "Средняя (30cm)"},
        }

    answer_callback_query_called = False
    delete_message_called = False
    send_message_calls = []

    def answer_callback_query(callback_query_id: str, **kwargs) -> dict:
        assert callback_query_id == "test_callback_id"
        nonlocal answer_callback_query_called
        answer_callback_query_called = True
        return {"ok": True}

    def deleteMessage(chat_id: int, message_id: int) -> dict:
        assert chat_id == 12345
        assert message_id == 100
        nonlocal delete_message_called
        delete_message_called = True
        return {"ok": True}

    def sendMessage(chat_id: int, text: str, **kwargs) -> dict:
        assert chat_id == 12345
        send_message_calls.append({"text": text, "kwargs": kwargs})
        return {"ok": True}

    mock_storage = Mock(
        {
            "update_user_data": update_user_data,
            "update_user_state": update_user_state,
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
    dispatcher.add_handlers(DrinkSelection())
    dispatcher.dispatch(test_update)

    assert update_user_data_called
    assert update_user_state_called
    assert answer_callback_query_called
    assert delete_message_called
    assert len(send_message_calls) == 1
    assert "Ваш заказ:" in send_message_calls[0]["text"]
    assert "Margherita" in send_message_calls[0]["text"]
    assert "Средняя (30cm)" in send_message_calls[0]["text"]
    assert "Coca-Cola" in send_message_calls[0]["text"]
