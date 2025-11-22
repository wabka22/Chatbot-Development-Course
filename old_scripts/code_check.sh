#!/bin/bash
# set -e

echo "🎨 === ПРОВЕРКА КОДА PIZZA BOT В DOCKER ==="

if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен!"
    exit 1
fi

echo "🚀 Сборка Docker-образа..."
docker build -t pizza-bot-codecheck .

echo "🧪 Запуск ruff и black..."
docker run --rm -v "$PWD":/app pizza-bot-codecheck \
    sh -c "ruff check . && black --check ."

CHECK_RESULT=$?
if [ $CHECK_RESULT -ne 0 ]; then
    echo "⚠️  Найдены проблемы с форматированием, исправляем автоматически..."
    
    echo "🔧 Запуск автоматического исправления..."
    docker run --rm -v "$PWD":/app pizza-bot-codecheck \
        sh -c "ruff check --fix . && black ."
    
    echo "✅ Автоматическое исправление завершено!"
    
    echo "🔍 Повторная проверка после исправления..."
    docker run --rm -v "$PWD":/app pizza-bot-codecheck \
        sh -c "ruff check . && black --check ."
    
    FINAL_RESULT=$?
    if [ $FINAL_RESULT -eq 0 ]; then
        echo "🎉 Все проблемы исправлены! Код соответствует стандартам."
    else
        echo "❌ Некоторые проблемы требуют ручного исправления."
        exit 1
    fi
else
    echo "✅ Код соответствует всем стандартам! Проверка завершена."
fi

echo "✅ Проверка кода завершена!"