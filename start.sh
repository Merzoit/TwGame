#!/bin/bash

# Установка зависимостей
pip install -r requirements.txt

# Переход в папку Django приложения
cd game_app

# Выполнение миграций
python manage.py migrate

# Сбор статических файлов
python manage.py collectstatic --noinput

# Запуск Django сервера (используем PORT из Railway или 8000 по умолчанию)
PORT=${PORT:-8000}
exec /opt/venv/bin/gunicorn twgame.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --threads 1 --log-level info
