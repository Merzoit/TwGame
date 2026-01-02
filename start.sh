#!/bin/bash

# Установка зависимостей
pip install -r requirements.txt

# Переход в папку Django приложения
cd game_app

# Выполнение миграций
python manage.py migrate

# Копирование статических файлов
mkdir -p static/images
cp ../../images/*.jpg static/images/ 2>/dev/null || echo "Images not found, skipping"

# Сбор статических файлов
python manage.py collectstatic --noinput --clear

# Возврат в корневую директорию
cd ..

# Запуск supervisor для управления процессами
exec supervisord -c supervisord.conf
