from django.apps import AppConfig
from django.db import connection


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        """Создание суперпользователя при запуске приложения"""
        try:
            # Проверяем, что база данных доступна
            cursor = connection.cursor()
            cursor.execute("SELECT 1")

            # Импортируем здесь, чтобы избежать циклических зависимостей
            from django.contrib.auth.models import User
            from django.core.management.color import no_style
            from django.db import transaction

            username = 'admin'
            email = 'admin@twgame.com'
            password = 'admin123'

            # Создаем суперпользователя в транзакции
            with transaction.atomic():
                if not User.objects.filter(username=username).exists():
                    user = User.objects.create_superuser(
                        username=username,
                        email=email,
                        password=password
                    )
                    print(f"Superuser '{username}' created successfully")
                else:
                    # Обновляем пароль на всякий случай
                    user = User.objects.get(username=username)
                    user.set_password(password)
                    user.save()
                    print(f"Superuser '{username}' password updated")

        except Exception as e:
            # Не логируем ошибки здесь, чтобы не засорять логи
            # Это нормально при первой миграции
            pass
