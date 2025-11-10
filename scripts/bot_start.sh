#!/bin/bash

echo "Запуск Pizza Bot с Docker Compose..."
echo "Используются переменные из .env файла"

# Проверяем наличие .env файла
if [ ! -f ".env" ]; then
    echo "ОШИБКА: Файл .env не найден!"
    echo "Создай файл .env с переменными окружения"
    exit 1
fi

# Загружаем переменные из .env
set -a
source .env
set +a

# Проверяем обязательные переменные
if [ -z "$TELEGRAM_TOKEN" ] || [ "$TELEGRAM_TOKEN" = "твой_настоящий_токен_от_botfather" ]; then
    echo "ОШИБКА: TELEGRAM_TOKEN не установлен в .env файле!"
    echo "Получи токен от @BotFather в Telegram и добавь в .env"
    exit 1
fi

echo "Переменные окружения:"
echo "POSTGRES_USER: $POSTGRES_USER"
echo "POSTGRES_DATABASE: $POSTGRES_DATABASE"
echo "POSTGRES_PORT: $POSTGRES_PORT"

# Запускаем Docker Compose
docker compose up --build