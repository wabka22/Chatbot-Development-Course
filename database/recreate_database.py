import sqlite3
import os
from dotenv import load_dotenv

def recreate_database() -> None:
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    load_dotenv(env_path)
    
    with sqlite3.connect(os.getenv('SQLITE_DATABASE_PATH')) as connection:
        connection.execute("DROP TABLE IF EXISTS telegram_updates")
        connection.execute("DROP TABLE IF EXISTS users")        
        connection.execute(
            """
            CREATE TABLE telegram_updates
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payload TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE users
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                state TEXT DEFAULT NULL,
                data TEXT DEFAULT NULL
            )
            """
        )
    print("База данных успешно создана!")

recreate_database()