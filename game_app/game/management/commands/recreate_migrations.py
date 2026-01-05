from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
import os
import shutil


class Command(BaseCommand):
    help = 'Удаляет все миграции и создает новые заново'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Удаляем все существующие миграции...'))

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
        deleted_count = 0
        for app in apps_to_reset:
            migrations_dir = os.path.join(settings.BASE_DIR, app, 'migrations')
            if os.path.exists(migrations_dir):
                # Оставляем только __init__.py
                for filename in os.listdir(migrations_dir):
                    if filename != '__init__.py' and filename.endswith('.py'):
                        filepath = os.path.join(migrations_dir, filename)
                        os.remove(filepath)
                        deleted_count += 1
                        self.stdout.write(f'  Удален: {app}/migrations/{filename}')

        self.stdout.write(self.style.SUCCESS(f'Удалено {deleted_count} миграционных файлов'))

        # Очищаем кэш
        self.stdout.write('Очищаем кэш Python...')
        cache_dirs = [
            os.path.join(settings.BASE_DIR, '__pycache__'),
        ]

        for app in apps_to_reset:
            cache_dirs.append(os.path.join(settings.BASE_DIR, app, '__pycache__'))

        for cache_dir in cache_dirs:
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir)
                self.stdout.write(f'  Очищен: {cache_dir}')

        # Создаем новые миграции
        self.stdout.write(self.style.SUCCESS('Создаем новые миграции...'))
        try:
            call_command('makemigrations', verbosity=1)
            self.stdout.write(self.style.SUCCESS('✅ Новые миграции созданы'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Ошибка при создании миграций: {e}'))
            return

        self.stdout.write(self.style.SUCCESS('🎯 Миграции готовы к применению!'))
        self.stdout.write(self.style.WARNING('Теперь выполните: python manage.py migrate'))
