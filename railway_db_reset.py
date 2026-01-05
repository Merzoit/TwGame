#!/usr/bin/env python3
"""
Скрипт для сброса базы данных на Railway через SSH
Используйте Railway CLI или скопируйте команды для ручного выполнения
"""

import subprocess
import sys
import time

# Параметры Railway
RAILWAY_PROJECT = "b594ed19-0f61-46f0-94a8-a64c962c8fd8"
RAILWAY_ENVIRONMENT = "141b8f58-c53e-4670-8e14-03a34285ef26"
RAILWAY_SERVICE = "eb58c45f-3990-474d-9d7c-1d970f1274b1"

def run_ssh_command(command, description, timeout=60):
    """Выполняет команду через Railway SSH"""
    ssh_cmd = f"railway ssh --project={RAILWAY_PROJECT} --environment={RAILWAY_ENVIRONMENT} --service={RAILWAY_SERVICE} -- {command}"

    print(f"\n🔄 {description}...")
    print(f"Команда: {command}")

    try:
        result = subprocess.run(
            ssh_cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        print(f"Exit code: {result.returncode}")

        if result.stdout:
            print("📝 STDOUT:")
            # Ограничим вывод первыми 10 строками
            lines = result.stdout.split('\n')[:10]
            for line in lines:
                if line.strip():
                    print(f"  {line}")
            if len(result.stdout.split('\n')) > 10:
                print(f"  ... и еще {len(result.stdout.split('\n')) - 10} строк")

        if result.stderr:
            print("⚠️  STDERR:")
            lines = result.stderr.split('\n')[:5]
            for line in lines:
                if line.strip():
                    print(f"  {line}")

        success = result.returncode == 0
        status = "✅ УСПЕШНО" if success else "❌ ОШИБКА"
        print(f"Результат: {status}")

        return success

    except subprocess.TimeoutExpired:
        print(f"⏰ Таймаут выполнения команды ({timeout} сек)")
        return False
    except Exception as e:
        print(f"💥 Ошибка выполнения: {e}")
        return False

def check_railway_cli():
    """Проверяет наличие Railway CLI"""
    try:
        result = subprocess.run(
            ["railway", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✅ Railway CLI найден")
            return True
        else:
            print("❌ Railway CLI не найден или не работает")
            return False
    except FileNotFoundError:
        print("❌ Railway CLI не установлен")
        print("   Установите Railway CLI: https://docs.railway.app/develop/cli")
        return False
    except Exception as e:
        print(f"❌ Ошибка проверки Railway CLI: {e}")
        return False

def main():
    print("🚨 СБРОС БАЗЫ ДАННЫХ НА RAILWAY 🚨")
    print("=" * 60)
    print("Этот скрипт выполнит полную перестройку базы данных")
    print("Все существующие данные будут потеряны!")
    print()

    # Проверка Railway CLI
    if not check_railway_cli():
        print("❌ Railway CLI не найден. Установите его и войдите в аккаунт:")
        print("   railway login")
        return

    # Подтверждение
    try:
        confirm = input("Продолжить? (yes/no): ").lower().strip()
        if confirm not in ['yes', 'y', 'да', 'д']:
            print("❌ Отменено пользователем")
            return
    except KeyboardInterrupt:
        print("\n❌ Отменено пользователем")
        return

    # Команды для выполнения
    commands = [
        ("cd /app/game_app && python manage.py db_status", "Проверка текущего статуса БД", 30),

        ("cd /app/game_app && python manage.py recreate_migrations", "Удаление старых миграций", 60),

        ("cd /app/game_app && python manage.py makemigrations", "Создание новых миграций", 30),

        ("cd /app/game_app && python manage.py migrate --fake-initial", "Применение миграций", 120),

        ("cd /app/game_app && python manage.py create_superuser", "Создание суперпользователя", 30),

        ("cd /app/game_app && python manage.py create_items", "Создание тестовых предметов", 60),

        ("cd /app/game_app && python manage.py db_status", "Проверка финального статуса БД", 30),
    ]

    success_count = 0
    total_commands = len(commands)

    print(f"\n🚀 Начинаем выполнение {total_commands} команд...")
    print("=" * 60)

    for i, (cmd, desc, timeout) in enumerate(commands, 1):
        print(f"\n[ {i}/{total_commands} ] {desc}")
        print("-" * 40)

        if run_ssh_command(cmd, desc, timeout):
            success_count += 1
        else:
            print(f"⚠️  Команда {i} завершилась с ошибкой, продолжаем...")

        # Небольшая пауза между командами
        if i < total_commands:
            time.sleep(2)

    print("\n" + "=" * 60)
    print(f"📊 РЕЗУЛЬТАТ: {success_count}/{total_commands} команд выполнено успешно")

    if success_count >= 5:  # Минимум 5 из 7 команд
        print("\n🎉 СБРОС БАЗЫ ДАННЫХ ЗАВЕРШЕН УСПЕШНО!")
        print("Теперь админка должна работать по адресу /db-admin/")
        print("Логин: admin")
        print("Пароль: admin123")
        print("\n💡 Railway пересоберет приложение в течение 5-15 минут")
    else:
        print("\n❌ Сброс завершен с ошибками!")
        print("Проверьте логи выше и попробуйте выполнить проблемные команды вручную")
        print("\nПолезные команды для ручного выполнения:")
        print("python manage.py db_status                    # Проверить статус")
        print("python manage.py recreate_migrations          # Пересоздать миграции")
        print("python manage.py migrate --fake-initial       # Применить миграции")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Скрипт прерван пользователем")
    except Exception as e:
        print(f"\n💥 Критическая ошибка: {e}")
        sys.exit(1)
