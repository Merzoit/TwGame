from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
from django.conf import settings
import os
import shutil


class Command(BaseCommand):
    help = 'Полный сброс базы данных и пересоздание миграций'

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-migrations',
            action='store_true',
            help='Не создавать новые миграции, только сбросить БД',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('🚨 НАЧИНАЕМ ПОЛНЫЙ СБРОС БАЗЫ ДАННЫХ 🚨'))
        self.stdout.write(self.style.WARNING('Все данные будут потеряны!'))

        # Получаем список всех приложений
        apps_to_reset = [
            'accounts',
            'characters',
            'items',
            'game',
            'core',
            'admin_panel',
            'api',
            'telegram_bot',
            'twitch_integration'
        ]

        # Удаляем все миграции
        self.stdout.write('Удаляем старые миграции...')
        for app in apps_to_reset:
            migrations_dir = os.path.join(settings.BASE_DIR, app, 'migrations')
            if os.path.exists(migrations_dir):
                # Оставляем только __init__.py
                for filename in os.listdir(migrations_dir):
                    if filename != '__init__.py' and filename.endswith('.py'):
                        filepath = os.path.join(migrations_dir, filename)
                        os.remove(filepath)
                        self.stdout.write(f'  Удален: {app}/migrations/{filename}')

        # Очищаем кэш Django
        self.stdout.write('Очищаем кэш Django...')
        cache_dir = os.path.join(settings.BASE_DIR, '__pycache__')
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)

        # Очищаем кэш приложений
        for app in apps_to_reset:
            cache_dir = os.path.join(settings.BASE_DIR, app, '__pycache__')
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir)

        # Сбрасываем базу данных
        self.stdout.write('Сбрасываем базу данных...')
        with connection.cursor() as cursor:
            try:
                # Для PostgreSQL
                cursor.execute("DROP SCHEMA public CASCADE;")
                cursor.execute("CREATE SCHEMA public;")
                cursor.execute("GRANT ALL ON SCHEMA public TO postgres;")
                cursor.execute("GRANT ALL ON SCHEMA public TO public;")
                self.stdout.write(self.style.SUCCESS('✅ PostgreSQL: Схема сброшена'))
            except Exception as e:
                try:
                    # Для SQLite
                    cursor.execute("DROP TABLE IF EXISTS django_migrations;")
                    cursor.execute("DROP TABLE IF EXISTS django_content_type;")
                    cursor.execute("VACUUM;")
                    self.stdout.write(self.style.SUCCESS('✅ SQLite: База данных очищена'))
                except Exception as e2:
                    self.stdout.write(self.style.WARNING(f'⚠️  Не удалось сбросить БД: {e} / {e2}'))

        # Создаем новые миграции
        if not options['no_migrations']:
            self.stdout.write('Создаем новые миграции...')
            try:
                call_command('makemigrations', verbosity=2)
                self.stdout.write(self.style.SUCCESS('✅ Миграции созданы'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Ошибка при создании миграций: {e}'))

        # Применяем миграции
        self.stdout.write('Применяем миграции...')
        try:
            call_command('migrate', verbosity=2)
            self.stdout.write(self.style.SUCCESS('✅ Миграции применены'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Ошибка при применении миграций: {e}'))

        # Создаем суперпользователя
        self.stdout.write('Создаем суперпользователя...')
        try:
            call_command('create_superuser', verbosity=1)
            self.stdout.write(self.style.SUCCESS('✅ Суперпользователь создан'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Ошибка при создании суперпользователя: {e}'))

        # Создаем тестовые предметы
        self.stdout.write('Создаем тестовые предметы...')
        try:
            call_command('create_items', verbosity=1)
            self.stdout.write(self.style.SUCCESS('✅ Тестовые предметы созданы'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Ошибка при создании предметов: {e}'))

        self.stdout.write(self.style.SUCCESS('🎉 ПОЛНЫЙ СБРОС БАЗЫ ДАННЫХ ЗАВЕРШЕН! 🎉'))
        self.stdout.write(self.style.SUCCESS('Можете перезапускать сервер!'))
