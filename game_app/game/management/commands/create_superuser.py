from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import connection
from django.conf import settings
import time


class Command(BaseCommand):
    help = 'Creates a superuser if it does not exist'

    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@twgame.com'
        password = 'admin123'

        # Ждем доступности базы данных
        max_attempts = 10
        for attempt in range(max_attempts):
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT 1")
                cursor.fetchone()
                self.stdout.write(self.style.SUCCESS("Database connection OK"))
                break
            except Exception as e:
                if attempt == max_attempts - 1:
                    self.stdout.write(
                        self.style.ERROR(f"Database connection failed after {max_attempts} attempts: {e}")
                    )
                    return
                self.stdout.write(f"Waiting for database... attempt {attempt + 1}/{max_attempts}")
                time.sleep(2)

        try:
            # Проверяем существующего пользователя
            existing_user = User.objects.filter(username=username).first()
            if existing_user:
                self.stdout.write(
                    self.style.WARNING(f'Superuser "{username}" already exists')
                )
                # Обновляем пароль на всякий случай
                existing_user.set_password(password)
                existing_user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Password updated for superuser "{username}"')
                )
                return

            # Создаем нового суперпользователя
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )

            self.stdout.write(
                self.style.SUCCESS(f'Superuser "{username}" created successfully with ID {user.id}')
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Failed to create superuser: {e}')
            )
            # Пробуем создать пользователя обычным способом
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    is_staff=True,
                    is_superuser=True
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Superuser "{username}" created with create_user method')
                )
            except Exception as e2:
                self.stdout.write(
                    self.style.ERROR(f'Failed to create superuser with create_user: {e2}')
                )
