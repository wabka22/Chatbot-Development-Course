from bot.bot_core.dispatcher import Dispatcher
from bot.handlers.order_result import OrderResult
from tests.mocks import Mock


def test_order_result_approve():
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
            "data": "order_approve",
        },
    }

    update_user_state_called = False

    def update_user_state(telegram_id: int, state: str) -> None:
        assert telegram_id == 12345
        assert state == "ORDER_FINISHED"
        nonlocal update_user_state_called
        update_user_state_called = True

    def get_user(telegram_id: int) -> dict | None:
        assert telegram_id == 12345
        return {
            "state": "WAIT_FOR_ORDER_APPROVE",
            "data": {
                "pizza_name": "Margherita",
                "pizza_size": "Средняя (30cm)",
                "drink": "Coca-Cola",
            },
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
    dispatcher.add_handlers(OrderResult())
    dispatcher.dispatch(test_update)

    assert update_user_state_called
    assert answer_callback_query_called
    assert delete_message_called
    assert len(send_message_calls) == 1
    assert "Заказ подтвержден" in send_message_calls[0]["text"]
    assert "Margherita" in send_message_calls[0]["text"]


def test_order_result_restart():
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
            "data": "order_restart",
        },
    }

    clear_user_data_called = False
    update_user_state_called = False

    def clear_user_data(telegram_id: int) -> None:
        assert telegram_id == 12345
        nonlocal clear_user_data_called
        clear_user_data_called = True

    def update_user_state(telegram_id: int, state: str) -> None:
        assert telegram_id == 12345
        nonlocal update_user_state_called
        update_user_state_called = True

    def get_user(telegram_id: int) -> dict | None:
        assert telegram_id == 12345
        return {"state": "WAIT_FOR_ORDER_APPROVE", "data": {}}

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
            "clear_user_data": clear_user_data,
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
    dispatcher.add_handlers(OrderResult())
    dispatcher.dispatch(test_update)

    assert clear_user_data_called
    assert update_user_state_called
    assert answer_callback_query_called
    assert delete_message_called
    assert len(send_message_calls) == 2
    assert "новый заказ" in send_message_calls[0]["text"]
    assert "выберите тип пиццы" in send_message_calls[1]["text"]
