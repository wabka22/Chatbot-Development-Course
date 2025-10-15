import json
import urllib.request
import os

from dotenv import load_dotenv

load_dotenv()


def makeRequest(method: str, **kwargs) -> dict:
    json_data = json.dumps(kwargs).encode('utf-8')

    request = urllib.request.Request(
        method='POST',
        url=f"{os.getenv("TELEGRAM_TOKEN")}/{method}",
        data=json_data,
        headers={'Content-Type': 'application/json',},
    )

    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode('utf-8')
        response_json = json.loads(response_body)
        assert response_json["ok"] == True
        return response_json["result"]


def getUpdates(**params) -> dict:
    return makeRequest("getUpdates", **params)


def sendMessage(chat_id: int, text: str,**params) -> dict:
    return makeRequest("sendMessage", chat_id=chat_id, text=text,**params)

def sendPhoto(chat_id: int, photo: str, **params) -> dict:
    return makeRequest("sendPhoto", chat_id=chat_id, photo=photo, **params)

def sendSticker(chat_id: int, sticker: str, **params) -> dict:
    return makeRequest("sendSticker", chat_id=chat_id, sticker=sticker, **params)

def sendVoice(chat_id: int, voice: str, **params) -> dict:
    return makeRequest("sendVoice", chat_id=chat_id, voice=voice, **params)

def sendDocument(chat_id: int, document: str, **params) -> dict:
    return makeRequest("sendDocument", chat_id=chat_id, document=document, **params)

def sendVideo(chat_id: int, video: str, **params) -> dict:
    return makeRequest("sendVideo", chat_id=chat_id, video=video, **params)

def getMe() -> dict:
    return makeRequest("getMe")
