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

def ensure_user_exists(telegram_id :int) -> None:
    with sqlite3.connect(os.getenv('SQLITE_DATABASE_PATH')) as connection:
        cursor= connection.execute
