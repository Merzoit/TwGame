#!/bin/bash

# Установка зависимостей
pip install -r requirements.txt

# Переход в папку Django приложения
cd game_app

# Выполнение миграций
python manage.py migrate

# Копирование статических файлов
echo "Setting up static files..."
mkdir -p static/images
echo "Copying images..."
cp ../../images/*.jpg static/images/ 2>/dev/null || echo "Warning: Images not found in ../../images/"
echo "Static files setup:"
ls -la static/images/ || echo "Warning: Static images directory not accessible"
echo "Project structure:"
ls -la ../../images/ 2>/dev/null || echo "Warning: Source images directory not found"

# Сбор статических файлов
python manage.py collectstatic --noinput --clear

# Возврат в корневую директорию
cd ..

# Запуск supervisor для управления процессами
exec supervisord -c supervisord.conf
