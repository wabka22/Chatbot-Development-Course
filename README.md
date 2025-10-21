Chatbot-Development-Course
--------------------------------
```bash
# Скачивание репозитория
git clone https://github.com/wabka22/Chatbot-Development-Course
```
```bash
# Копирование примера файла окружения и его редактирование
cd Chatbot-Development-Course && cp .env.base .env
```
```bash
# Запуск скрипта(один раз при скачивании)
source ./scripts/setup.sh
```
```bash
# Инициализация базы данных
python3 -m bot.recreate_database
```
```bash
# Запуск бота
python3 -m bot
```
```bash
# база данных
sqlite3 <database>.sqlite
```
```bash
# просмотр содержимого 
watch -n 1 "sqlite3 -cmd '.mode box' -cmd '.headers on' <database>.sqlite 'SELECT * FROM users ORDER BY id DESC LIMIT 1;'"
```
