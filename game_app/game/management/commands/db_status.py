from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management import call_command
from io import StringIO


class Command(BaseCommand):
    help = 'Показывает статус базы данных и миграций'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('📊 СТАТУС БАЗЫ ДАННЫХ 📊'))
        self.stdout.write('=' * 50)

        # Проверяем подключение к БД
        self.stdout.write('🔍 Проверка подключения к БД...')
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                self.stdout.write(self.style.SUCCESS('✅ Подключение к БД: OK'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Подключение к БД: FAILED - {e}'))
            return

        # Проверяем таблицы Django
        self.stdout.write('🔍 Проверка таблиц Django...')
        with connection.cursor() as cursor:
            try:
                # PostgreSQL
                cursor.execute("""
                    SELECT COUNT(*) FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_name LIKE '%'
                """)
                total_tables = cursor.fetchone()[0]

                cursor.execute("""
                    SELECT COUNT(*) FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_name LIKE 'game_app_%'
                """)
                app_tables = cursor.fetchone()[0]

                self.stdout.write(self.style.SUCCESS(f'✅ Всего таблиц: {total_tables}'))
                self.stdout.write(self.style.SUCCESS(f'✅ Таблиц приложения: {app_tables}'))

            except:
                # SQLite
                try:
                    cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
                    total_tables = cursor.fetchone()[0]

                    cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name LIKE 'game_app_%'")
                    app_tables = cursor.fetchone()[0]

                    self.stdout.write(self.style.SUCCESS(f'✅ Всего таблиц: {total_tables}'))
                    self.stdout.write(self.style.SUCCESS(f'✅ Таблиц приложения: {app_tables}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'❌ Ошибка проверки таблиц: {e}'))

        # Проверяем миграции
        self.stdout.write('🔍 Проверка статуса миграций...')
        try:
            # Перехватываем вывод команды showmigrations
            old_stdout = self.stdout
            self.stdout = StringIO()

            call_command('showmigrations', verbosity=0)

            migrations_output = self.stdout.getvalue()
            self.stdout = old_stdout

            applied_count = migrations_output.count('[X]')
            pending_count = migrations_output.count('[ ]')

            self.stdout.write(self.style.SUCCESS(f'✅ Примененных миграций: {applied_count}'))
            self.stdout.write(self.style.SUCCESS(f'⏳ Ожидающих миграций: {pending_count}'))

            if pending_count > 0:
                self.stdout.write(self.style.WARNING('⚠️  Есть непримененные миграции!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Ошибка проверки миграций: {e}'))

        # Проверяем суперпользователя
        self.stdout.write('🔍 Проверка суперпользователя...')
        from django.contrib.auth.models import User
        try:
            superusers = User.objects.filter(is_superuser=True)
            if superusers.exists():
                self.stdout.write(self.style.SUCCESS(f'✅ Суперпользователей: {superusers.count()}'))
                for user in superusers:
                    self.stdout.write(f'   👤 {user.username} ({user.email})')
            else:
                self.stdout.write(self.style.ERROR('❌ Суперпользователь не найден!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Ошибка проверки суперпользователя: {e}'))

        # Проверяем тестовые данные
        self.stdout.write('🔍 Проверка тестовых данных...')
        try:
            from accounts.models import Player
            from items.models import Item

            players_count = Player.objects.count()
            items_count = Item.objects.count()

            self.stdout.write(self.style.SUCCESS(f'✅ Игроков: {players_count}'))
            self.stdout.write(self.style.SUCCESS(f'✅ Предметов: {items_count}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Ошибка проверки данных: {e}'))

        self.stdout.write('=' * 50)
        self.stdout.write(self.style.SUCCESS('🎯 Проверка завершена!'))
