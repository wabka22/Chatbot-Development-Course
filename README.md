Chatbot-Development-Course
--------------------------------
```bash
# Скачивание репозитория
git clone https://github.com/wabka22/Chatbot-Development-Course
```
```bash
# Копирование примера файла окружения и его редактирование
cp .env.base .env
```
```bash
# Запуск тестов
source ./scripts/test_start.sh
```
```bash
# Запуск бота
source ./scripts/bot_start.sh
```
```bash
# просмотр содержимого 
watch -n 1 "sqlite3 -cmd '.mode box' -cmd '.headers on' <database>.sqlite 'SELECT * FROM users ORDER BY id DESC LIMIT 1;'"
```


docker compose up -d

docker compose down

docker compose exec postgres psql -U postgres -d pizza_bot
