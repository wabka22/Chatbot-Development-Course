#!/bin/bash

echo "Активация виртуального окружения..."
source .venv/bin/activate

echo "Установка зависимостей..."
pip install -r requirements.txt

echo "Инициализация базы данных..."
python3 -m bot.recreate_database

echo "Запуск бота..."
python3 -m bot