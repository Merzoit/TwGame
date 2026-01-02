#!/bin/bash

# Установка зависимостей
pip install -r requirements.txt

# Переход в папку Django приложения
cd game_app

# Выполнение миграций
python manage.py migrate

# Сбор статических файлов
python manage.py collectstatic --noinput

# Возврат в корневую директорию
cd ..

# Запуск supervisor для управления процессами
exec supervisord -c supervisord.conf
