#!/bin/bash
set -e

# -------------------------------
# Pizza Bot — запуск с Docker Compose
# -------------------------------

echo "🍕 === Запуск Pizza Bot ==="

# Проверяем наличие .env
if [ ! -f ".env" ]; then
    echo "❌ Файл .env не найден!"
    echo "Создай его на основе .env.example:"
    echo "  cp .env.example .env"
    exit 1
fi

# Загружаем переменные окружения
set -a
source .env
set +a

# Проверяем TELEGRAM_TOKEN
if [ -z "$TELEGRAM_TOKEN" ] || [ "$TELEGRAM_TOKEN" = "твой_настоящий_токен_от_botfather" ]; then
    echo "❌ TELEGRAM_TOKEN не установлен или некорректен!"
    echo "👉 Получи токен от @BotFather и добавь его в .env"
    exit 1
fi

# Проверяем Docker Compose
if ! command -v docker compose &> /dev/null; then
    echo "❌ Команда 'docker compose' не найдена!"
    echo "Установи Docker Compose v2+"
    exit 1
fi

# Обрабатываем аргументы
COMMAND=$1

case "$COMMAND" in
  up|"")
    echo "🚀 Запуск Docker Compose..."
    docker compose up -d --build
    echo "✅ Бот запущен!"
    ;;
  down)
    echo "🧹 Остановка и удаление контейнеров..."
    docker compose down
    ;;
  restart)
    echo "🔁 Перезапуск Pizza Bot..."
    docker compose down
    docker compose up -d --build
    ;;
  logs)
    echo "📜 Просмотр логов:"
    docker compose logs -f
    ;;
  *)
    echo "Использование: $0 [up|down|restart|logs]"
    exit 1
    ;;
esac
