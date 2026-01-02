#!/bin/bash

# Установка зависимостей
pip install -r requirements.txt

# Переход в папку Django приложения
cd game_app

# Выполнение миграций
python manage.py migrate

# Копирование статических файлов
echo "Setting up static files..."
mkdir -p game_app/static/images
echo "Copying images..."
cp images/*.jpg game_app/static/images/ 2>/dev/null || echo "Warning: Images not found in images/"
echo "Static files setup:"
ls -la game_app/static/images/ || echo "Warning: Static images directory not accessible"

# Сбор статических файлов
python manage.py collectstatic --noinput --clear

# Возврат в корневую директорию
cd ..

# Запуск supervisor для управления процессами
exec supervisord -c supervisord.conf
