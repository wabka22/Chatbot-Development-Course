from bot.dispatcher import Dispatcher
from bot.handlers.message_echo import MessageEcho
from bot.handlers.message_photo_echo import MessagePhotoEcho
from bot.handlers.video_echo import VideoEcho
from bot.handlers.voice_echo import VoiceEcho
from bot.handlers.sticker_echo import StickerEcho
from bot.handlers.document_echo import DocumentEcho
from bot.handlers.database_logger import DatabaseLogger
from bot.long_polling import start_long_polling

if __name__ == "__main__":
    try:
        dispatcher= Dispatcher()
        dispatcher.add_handler(DatabaseLogger())
        dispatcher.add_handler(MessageEcho())
        dispatcher.add_handler(MessagePhotoEcho())
        dispatcher.add_handler(VideoEcho())
        dispatcher.add_handler(VoiceEcho())
        dispatcher.add_handler(StickerEcho())
        dispatcher.add_handler(DocumentEcho())
        start_long_polling(dispatcher)
    except KeyboardInterrupt:
      print("Thank you! The bot is disabled")
