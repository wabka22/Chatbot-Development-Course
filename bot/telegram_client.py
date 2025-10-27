import json
import urllib.request
import os

from dotenv import load_dotenv

load_dotenv()


def makeRequest(method: str, **kwargs) -> dict:
    json_data = json.dumps(kwargs).encode("utf-8")

    request = urllib.request.Request(
        method="POST",
        url=f"{os.getenv("TELEGRAM_TOKEN")}/{method}",
        data=json_data,
        headers={
            "Content-Type": "application/json",
        },
    )

    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")
        response_json = json.loads(response_body)
        assert response_json["ok"]
        return response_json["ok"]


def getUpdates(**params) -> dict:
    return makeRequest("getUpdates", **params)


def getMe() -> dict:
    return makeRequest("getMe")


def answer_callback_query(callback_query_id: str, **params) -> dict:
    return makeRequest(
        "answerCallbackQuery", callback_query_id=callback_query_id, **params
    )


def sendMessage(chat_id: int, text: str, **params) -> dict:
    return makeRequest("sendMessage", chat_id=chat_id, text=text, **params)


def deleteMessage(chat_id: int, message_id: int, **params) -> dict:
    return makeRequest(
        "deleteMessage", chat_id=chat_id, message_id=message_id, **params
    )
