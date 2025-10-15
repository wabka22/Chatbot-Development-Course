from bot.handler import Handler
import sqlite3
import json
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseLogger(Handler):
    def can_handle(self, update: dict) -> bool:
        return True
    
    def handle(self, update: dict) -> bool:
        connection = sqlite3.connect(os.getenv('SQLITE_DATABASE_PATH'))
        with connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS telegram_updates
                (
                    id INTEGER PRIMARY KEY,
                    payload TEXT NOT NULL
                )
                """
            )
            
            connection.execute(
                "INSERT INTO telegram_updates (payload) VALUES (?)",
                (json.dumps(update, ensure_ascii=False, indent=2),)
            )
        connection.close()
        
        return True