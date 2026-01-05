#!/bin/bash
# Ручные команды для сброса БД на Railway
# Выполняйте по одной в Railway SSH

echo "🚨 РУЧНЫЕ КОМАНДЫ ДЛЯ СБРОСА БД НА RAILWAY 🚨"
echo "=============================================="

echo ""
echo "1. Проверка статуса БД:"
echo "railway ssh --project=b594ed19-0f61-46f0-94a8-a64c962c8fd8 --environment=141b8f58-c53e-4670-8e14-03a34285ef26 --service=eb58c45f-3990-474d-9d7c-1d970f1274b1"
echo "cd /app/game_app && python manage.py db_status"
echo ""

echo "2. Удаление старых миграций:"
echo "railway ssh --project=b594ed19-0f61-46f0-94a8-a64c962c8fd8 --environment=141b8f58-c53e-4670-8e14-03a34285ef26 --service=eb58c45f-3990-474d-9d7c-1d970f1274b1"
echo "cd /app/game_app && python manage.py recreate_migrations"
echo ""

echo "3. Создание новых миграций:"
echo "railway ssh --project=b594ed19-0f61-46f0-94a8-a64c962c8fd8 --environment=141b8f58-c53e-4670-8e14-03a34285ef26 --service=eb58c45f-3990-474d-9d7c-1d970f1274b1"
echo "cd /app/game_app && python manage.py makemigrations"
echo ""

echo "4. Применение миграций:"
echo "railway ssh --project=b594ed19-0f61-46f0-94a8-a64c962c8fd8 --environment=141b8f58-c53e-4670-8e14-03a34285ef26 --service=eb58c45f-3990-474d-9d7c-1d970f1274b1"
echo "cd /app/game_app && python manage.py migrate --fake-initial"
echo ""

echo "5. Создание суперпользователя:"
echo "railway ssh --project=b594ed19-0f61-46f0-94a8-a64c962c8fd8 --environment=141b8f58-c53e-4670-8e14-03a34285ef26 --service=eb58c45f-3990-474d-9d7c-1d970f1274b1"
echo "cd /app/game_app && python manage.py create_superuser"
echo ""

echo "6. Создание тестовых предметов:"
echo "railway ssh --project=b594ed19-0f61-46f0-94a8-a64c962c8fd8 --environment=141b8f58-c53e-4670-8e14-03a34285ef26 --service=eb58c45f-3990-474d-9d7c-1d970f1274b1"
echo "cd /app/game_app && python manage.py create_items"
echo ""

echo "7. Финальная проверка:"
echo "railway ssh --project=b594ed19-0f61-46f0-94a8-a64c962c8fd8 --environment=141b8f58-c53e-4670-8e14-03a34285ef26 --service=eb58c45f-3990-474d-9d7c-1d970f1274b1"
echo "cd /app/game_app && python manage.py db_status"
echo ""

echo "💡 СОВЕТЫ:"
echo "- Выполняйте команды по порядку"
echo "- После каждой команды проверяйте результат"
echo "- Если возникнут ошибки, сообщите мне"
echo "- После завершения админка будет доступна по /db-admin/"
