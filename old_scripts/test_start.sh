#!/bin/bash
# set -e

echo "🍕 === ЗАПУСК ТЕСТОВ PIZZA BOT В DOCKER ==="

# Проверка .env
if [ ! -f ".env" ]; then
    echo "❌ Файл .env не найден!"
    echo "Создай его на основе .env.example:"
    echo "  cp .env.example .env"
    exit 1
fi

set -a
source .env
set +a

# Проверка TELEGRAM_TOKEN
if [ -z "$TELEGRAM_TOKEN" ]; then
    echo "❌ TELEGRAM_TOKEN не установлен!"
    exit 1
fi

# Проверка Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен!"
    exit 1
fi

# Сборка Docker-образа
echo "🚀 Сборка Docker-образа..."
docker build -t pizza-bot-test .

# Запуск тестов внутри контейнера
echo "🧪 Запуск тестов в Docker..."
docker run --rm -e TELEGRAM_TOKEN="$TELEGRAM_TOKEN" -v "$PWD":/app pizza-bot-test pytest -v tests/

echo "✅ Тесты завершены!"
