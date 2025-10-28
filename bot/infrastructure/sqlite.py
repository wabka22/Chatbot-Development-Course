import json
import os
import sqlite3
from dotenv import load_dotenv
from bot.domain.storage import Storage

load_dotenv()


class SqliteStorage(Storage):

    def __init__(self):
        self.database_path = os.getenv("SQLITE_DATABASE_PATH")

    def persist_update(self, update: dict) -> None:
        with sqlite3.connect(self.database_path) as connection:
            connection.execute(
                "INSERT INTO telegram_updates (payload) VALUES (?)",
                (json.dumps(update, ensure_ascii=False, indent=2),),
            )

    def ensure_user_exists(self, telegram_id: int) -> None:
        with sqlite3.connect(self.database_path) as connection:
            with connection:
                cursor = connection.execute(
                    "SELECT 1 FROM users WHERE telegram_id = ?", (telegram_id,)
                )
                if cursor.fetchone() is None:
                    connection.execute(
                        "INSERT INTO users (telegram_id) VALUES (?)", (telegram_id,)
                    )

    def get_user(self, telegram_id: int) -> dict:
        with sqlite3.connect(self.database_path) as connection:
            with connection:
                cursor = connection.execute(
                    "SELECT id, telegram_id, created_at, state, data FROM users WHERE telegram_id = ?",
                    (telegram_id,),
                )
                result = cursor.fetchone()
                if result:
                    return {
                        "id": result[0],
                        "telegram_id": result[1],
                        "created_at": result[2],
                        "state": result[3],
                        "data": json.loads(result[4]) if result[4] else {},
                    }
                return None

    def update_user_state(self, telegram_id: int, state: str) -> None:
        with sqlite3.connect(self.database_path) as connection:
            with connection:
                connection.execute(
                    "UPDATE users SET state = ? WHERE telegram_id = ?",
                    (state, telegram_id),
                )

    def update_user_data(self, telegram_id: int, data: dict) -> None:
        with sqlite3.connect(self.database_path) as connection:
            with connection:
                connection.execute(
                    "UPDATE users SET data = ? WHERE telegram_id = ?",
                    (json.dumps(data, ensure_ascii=False, indent=2), telegram_id),
                )

    def clear_user_data(self, telegram_id: int) -> None:
        with sqlite3.connect(self.database_path) as connection:
            with connection:
                connection.execute(
                    "UPDATE users SET state = NULL, data = NULL WHERE telegram_id = ?",
                    (telegram_id,),
                )
