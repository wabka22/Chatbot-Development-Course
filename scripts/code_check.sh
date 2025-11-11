#!/bin/bash
set -e

echo "🎨 === ПРОВЕРКА КОДА PIZZA BOT В DOCKER ==="

# Проверка Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен!"
    exit 1
fi

# Сборка Docker-образа
echo "🚀 Сборка Docker-образа..."
docker build -t pizza-bot-codecheck .

# Запуск ruff и black внутри контейнера
echo "🧪 Запуск ruff и black..."
docker run --rm -v "$PWD":/app pizza-bot-codecheck \
    sh -c "ruff check . && black --check ."

echo "✅ Проверка кода завершена!"
