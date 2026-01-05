#!/bin/bash

echo "🚀 Starting Railway application..."

# Установка зависимостей (если не установлены)
pip install -r requirements.txt --quiet

# Переход в директорию Django проекта
cd game_app

# Применяем миграции
echo "📊 Applying database migrations..."
python manage.py migrate --noinput

# Создаем суперпользователя (если не существует)
echo "👤 Creating superuser..."
python manage.py create_superuser

# Создаем тестовые предметы
echo "🎮 Creating test items..."
python manage.py create_items

# Собираем статические файлы
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Настройка Telegram webhook (если скрипт существует)
if [ -f "../telegram_bot/main.py" ]; then
    echo "📱 Setting up Telegram webhook..."
    python ../telegram_bot/main.py &
fi

# Запуск Django сервера
echo "🌐 Starting Django server..."
python manage.py runserver 0.0.0.0:$PORT
