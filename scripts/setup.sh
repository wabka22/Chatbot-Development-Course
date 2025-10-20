#!/bin/bash

echo "Создание виртуального окружения..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "Виртуальное окружение создано"
else
    echo "Виртуальное окружение уже существует"
fi

echo "Активация виртуального окружения в текущей оболочке..."
source .venv/bin/activate

echo "Установка зависимостей..."
pip install -r requirements.txt

echo "Инициализация базы данных..."
python3 -m bot.recreate_database

echo "Запуск бота..."
python3 -m bot