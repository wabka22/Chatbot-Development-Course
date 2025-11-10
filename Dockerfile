#!/bin/bash

echo "=== ЗАПУСК ТЕСТОВ PIZZA BOT ==="

echo "Активация виртуального окружения..."
source .venv/bin/activate

echo "Запуск тестов..."
pytest -v tests/

if [ $? -eq 0 ]; then
    echo "✅ Все тесты прошли успешно! (8/8)"
else
    echo "❌ Некоторые тесты не прошли"
    exit 1
fi