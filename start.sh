#!/bin/bash

# Установка зависимостей
pip install -r requirements.txt

# Переход в папку Django приложения
cd game_app

# Пересоздание миграций (если нужно)
echo "Checking if migrations recreation is needed..."
if [ "$RECREATE_MIGRATIONS" = "true" ]; then
    echo "Recreating migrations..."
    python manage.py recreate_migrations
    echo "Migrations recreated"
fi

# Принудительное применение миграций
echo "Applying migrations..."
python manage.py force_migrate --fake-initial
echo "Migrations applied"

# Проверка статуса базы данных
echo "Checking database status..."
python manage.py db_status

# Создание суперпользователя
echo "Creating superuser..."
python manage.py create_superuser
echo "Superuser creation completed"

# Создание тестовых предметов
echo "Creating items..."
python manage.py create_items
echo "Items creation completed"

# Копирование статических файлов
echo "Setting up static files..."
mkdir -p game_app/static/images
echo "Copying images..."
cp images/*.jpg game_app/static/images/ 2>/dev/null || echo "Warning: Images not found in images/"
echo "Static files setup:"
ls -la game_app/static/images/ || echo "Warning: Static images directory not accessible"

# Сбор статических файлов
python manage.py collectstatic --noinput --clear

# Финальная проверка суперпользователя
echo "Final superuser check..."
python manage.py shell -c "
from django.contrib.auth.models import User
username = 'admin'
password = 'admin123'
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email='admin@twgame.com', password=password)
    print('Superuser created via shell')
else:
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
    print('Superuser password updated via shell')
print('Superuser check completed')
"

# Настройка Telegram webhook
echo "Setting up Telegram webhook..."
python ../telegram_bot/main.py

# Возврат в корневую директорию
cd ..

# Запуск supervisor для управления процессами
exec supervisord -c supervisord.conf
