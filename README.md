```bash
# Скачивание репозитория
git clone https://github.com/wabka22/Chatbot-Development-Course
```
```bash
# Копирование примера файла окружения и его редактирование
cp .env.base .env
```
```bash
# Скачивание make 
make install
```
```bash
# Запуск бота
source ./scripts/bot_start.sh
```
```bash
# Запуск контейнеров
docker compose up -d

# Остановка контейнеров
docker compose down

# Просмотр логов
docker compose logs -f telegram_bot'"
```
```bash
# Подключение к PostgreSQL
docker compose exec postgres psql -U postgres -d pizza_bot

# Просмотр последних пользователей (внутри psql)
SELECT * FROM users ORDER BY id DESC LIMIT 5;

# Просмотр логов базы данных в реальном времени
watch -n 1 "docker compose exec postgres psql -U postgres -d pizza_bot -c 'SELECT * FROM users ORDER BY id DESC LIMIT 1;'"
```