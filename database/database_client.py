import sqlite3
import os
import json

from dotenv import load_dotenv

load_dotenv()

def persist_update(update: dict) -> None:
    with sqlite3.connect(os.getenv('SQLITE_DATABASE_PATH')) as connection:
        connection.execute(
            "INSERT INTO telegram_updates (payload) VALUES (?)",
            (json.dumps(update, ensure_ascii=False, indent=2),)
        )

def recreate_database() -> None:
    with sqlite3.connect(os.getenv('SQLITE_DATABASE_PATH')) as connection:
        connection.execute("DROP TABLE IF EXISTS telegram_updates")
        connection.execute("DROP TABLE IF EXISTS users")        
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS telegram_updates
            (
                id INTEGER PRIMARY KEY,
                payload TEXT NOT NULL
            )
            """,
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users
            (
                id INTEGER PRIMARY KEY,
                telegram_id INTEGER NOT NULL UNIQUE
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                state TEXT DEFAULT NULL,
                data TEXT DEFAULT NULL
            )
            """,
        )

def ensure_user_exists(telegram_id: int) -> None:
    with sqlite3.connect(os.getenv("SQLITE_DATABASE_PATH")) as connection:
        with connection:
            cursor = connection.execute(
                "SELECT 1 FROM users WHERE telegram_id = ?", (telegram_id,)
            )
            if cursor.fetchone() is None:
                connection.execute(
                    "INSERT INTO users (telegram_id) VALUES (?)", (telegram_id,)
                )


def get_user(telegram_id: int) -> dict:
    with sqlite3.connect(os.getenv("SQLITE_DATABASE_PATH")) as connection:
        with connection:
            cursor = connection.execute(
                "SELECT id, telegram_id, created_at, state, data FROM users WHERE telegram_id = ?", (telegram_id,)
            )
            result = cursor.fetchone()
            if result:
                return {
                    'id': result[0],
                    'telegram_id': result[1],
                    'created_at': result[2],
                    'state': result[3],
                    'data': result[4]
                }
            return None


def update_user_state(telegram_id: int, state: str) -> None:
    with sqlite3.connect(os.getenv("SQLITE_DATABASE_PATH")) as connection:
        with connection:
            connection.execute(
                "UPDATE users SET state = ? WHERE telegram_id = ?",
                (state, telegram_id)
            )


def update_user_data(telegram_id: int, data: dict) -> None:
    with sqlite3.connect(os.getenv("SQLITE_DATABASE_PATH")) as connection:
        with connection:
            connection.execute(
                "UPDATE users SET data = ? WHERE telegram_id = ?",
                (json.dumps(data, ensure_ascii=False, indent=2), telegram_id)
            )


def clear_user_data(telegram_id: int) -> None:
    with sqlite3.connect(os.getenv("SQLITE_DATABASE_PATH")) as connection:
        with connection:
            connection.execute(
                "UPDATE users SET state = NULL, data = NULL WHERE telegram_id = ?",
                (telegram_id,)
            )