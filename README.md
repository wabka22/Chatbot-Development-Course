Chatbot-Development-Course
--------------------------------
```bash
# Копирование примера файла окружения и его редактирование
cp .env.base .env
```
```bash
# Создание виртуального окружения
python3 -m venv .venv
```
```bash
# Активация виртуального окружения
source .venv/bin/activate
```
```bash
# Установка зависимостей
pip install -r requirements.txt
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
# просмотр базы данных
sqlite3 <database>.sqlite
```