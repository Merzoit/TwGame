from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection


class Command(BaseCommand):
    help = 'Принудительное применение миграций с обработкой конфликтов'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fake-initial',
            action='store_true',
            help='Помечает initial миграции как fake',
        )

    def handle(self, *args, **options):
        self.stdout.write('Проверяем состояние базы данных...')

        # Проверяем, есть ли таблицы Django
        with connection.cursor() as cursor:
            try:
                cursor.execute("""
                    SELECT COUNT(*) FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_name LIKE 'game_app_%'
                """)
                existing_tables = cursor.fetchone()[0]
                self.stdout.write(f'Найдено {existing_tables} таблиц приложения')
            except:
                # Для SQLite
                try:
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'game_app_%'")
                    existing_tables = len(cursor.fetchall())
                    self.stdout.write(f'Найдено {existing_tables} таблиц приложения')
                except:
                    existing_tables = 0
                    self.stdout.write('Не удалось проверить существующие таблицы')

        if existing_tables > 0 and not options['fake_initial']:
            self.stdout.write(self.style.WARNING(
                f'⚠️  Найдено {existing_tables} существующих таблиц!'
            ))
            self.stdout.write(self.style.WARNING(
                'Используйте --fake-initial чтобы пометить initial миграции как примененные'
            ))
            return

        # Применяем миграции
        self.stdout.write('Применяем миграции...')
        try:
            if options['fake_initial']:
                call_command('migrate', verbosity=1, fake_initial=True)
                self.stdout.write(self.style.SUCCESS('✅ Миграции применены с --fake-initial'))
            else:
                call_command('migrate', verbosity=1)
                self.stdout.write(self.style.SUCCESS('✅ Миграции применены'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Ошибка при применении миграций: {e}'))
            return

        # Создаем суперпользователя
        self.stdout.write('Создаем суперпользователя...')
        try:
            call_command('create_superuser', verbosity=0)
            self.stdout.write(self.style.SUCCESS('✅ Суперпользователь создан'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'⚠️  Суперпользователь уже существует или ошибка: {e}'))

        # Создаем тестовые предметы
        self.stdout.write('Создаем тестовые предметы...')
        try:
            call_command('create_items', verbosity=0)
            self.stdout.write(self.style.SUCCESS('✅ Тестовые предметы созданы'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Ошибка при создании предметов: {e}'))

        self.stdout.write(self.style.SUCCESS('🎉 База данных готова к работе!'))
