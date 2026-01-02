#!/bin/bash

# Установка зависимостей
pip install -r requirements.txt

# Переход в папку Django приложения
cd game_app

# Выполнение миграций
python manage.py migrate

# Сбор статических файлов
python manage.py collectstatic --noinput

# Запуск сервера с Gunicorn
gunicorn twgame.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --threads 2
