FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ruff check . && black --check . && \
    python -m bot.bot_core.recreate_database_postgres && python -m bot
