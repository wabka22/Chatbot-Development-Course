#!/bin/bash
set -e

echo "🍕 === Запуск Pizza Bot ==="

if [ ! -f ".env" ]; then
    echo "❌ Файл .env не найден!"
    echo "Создай его на основе .env.example:"
    echo "  cp .env.example .env"
    exit 1
fi

set -a
source .env
set +a

if [ -z "$TELEGRAM_TOKEN" ]; then
    echo "❌ TELEGRAM_TOKEN не установлен!"
    exit 1
fi

if ! command -v docker compose &> /dev/null; then
    echo "❌ Команда 'docker compose' не найдена!"
    exit 1
fi

echo "🚀 Запуск Docker Compose..."
docker compose up -d --build
echo "✅ Бот запущен!"
