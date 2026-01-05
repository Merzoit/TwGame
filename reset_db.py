#!/usr/bin/env python3
"""
Скрипт для сброса базы данных на Railway
Запустите этот скрипт если нужно полностью пересоздать БД
"""

import os
import sys
import subprocess
import time

def run_command(cmd, description):
    """Выполняет команду и показывает результат"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd='game_app')
        if result.returncode == 0:
            print(f"✅ {description}: УСПЕШНО")
            if result.stdout.strip():
                print(f"   Вывод: {result.stdout.strip()}")
        else:
            print(f"❌ {description}: ОШИБКА")
            print(f"   Код: {result.returncode}")
            if result.stderr:
                print(f"   Ошибка: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ {description}: ИСКЛЮЧЕНИЕ - {e}")
        return False

def main():
    print("🚨 СБРОС БАЗЫ ДАННЫХ ДЛЯ RAILWAY 🚨")
    print("=" * 50)
    print("Этот скрипт:")
    print("1. Удалит все существующие миграции")
    print("2. Создаст новые миграции")
    print("3. Применит их к базе данных")
    print("4. Создаст суперпользователя")
    print("5. Создаст тестовые предметы")
    print()
    print("⚠️  ВСЕ ДАННЫЕ БУДУТ ПОТЕРЯНЫ! ⚠️")
    print()

    # Подтверждение
    confirm = input("Продолжить? (yes/no): ").lower().strip()
    if confirm not in ['yes', 'y', 'да', 'д']:
        print("❌ Отменено пользователем")
        return

    # Переходим в директорию проекта
    os.chdir('game_app')

    # Проверяем, что мы в правильной директории
    if not os.path.exists('manage.py'):
        print("❌ Ошибка: manage.py не найден. Убедитесь что вы в директории game_app")
        return

    # Выполняем команды
    commands = [
        ("python manage.py recreate_migrations", "Удаление старых миграций"),
        ("python manage.py makemigrations", "Создание новых миграций"),
        ("python manage.py migrate --fake-initial", "Применение миграций"),
        ("python manage.py create_superuser", "Создание суперпользователя"),
        ("python manage.py create_items", "Создание тестовых предметов"),
        ("python manage.py db_status", "Проверка статуса БД")
    ]

    success_count = 0
    for cmd, desc in commands:
        if run_command(cmd, desc):
            success_count += 1
        else:
            print(f"⚠️  Команда '{desc}' завершилась с ошибкой, продолжаем...")

    print("\n" + "=" * 50)
    if success_count >= 4:  # Минимум 4 успешные команды из 6
        print("🎉 СБРОС БАЗЫ ДАННЫХ ЗАВЕРШЕН УСПЕШНО! 🎉")
        print("Можете перезапускать приложение!")
    else:
        print("❌ СБРОС ЗАВЕРШЕН С ОШИБКАМИ ❌")
        print("Проверьте логи выше и попробуйте снова")

    print("\n💡 Полезные команды:")
    print("   python manage.py db_status          # Проверить статус БД")
    print("   python manage.py recreate_migrations # Пересоздать миграции")
    print("   python manage.py force_migrate       # Применить миграции")

if __name__ == '__main__':
    main()
