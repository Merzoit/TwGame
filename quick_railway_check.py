#!/usr/bin/env python3
"""
Быстрая проверка Railway CLI и статуса БД
"""

import subprocess
import sys

def check_railway_cli():
    """Проверяет Railway CLI"""
    print("🔍 Проверка Railway CLI...")
    try:
        result = subprocess.run(
            ["railway", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✅ Railway CLI найден")
            print(f"   Версия: {result.stdout.strip()}")
            return True
        else:
            print("❌ Railway CLI не работает корректно")
            return False
    except FileNotFoundError:
        print("❌ Railway CLI не установлен")
        print("   Установите: https://docs.railway.app/develop/cli")
        return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def check_railway_login():
    """Проверяет авторизацию в Railway"""
    print("\n🔍 Проверка авторизации в Railway...")
    try:
        result = subprocess.run(
            ["railway", "whoami"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✅ Авторизация успешна")
            return True
        else:
            print("❌ Не авторизованы в Railway")
            print("   Выполните: railway login")
            return False
    except Exception as e:
        print(f"❌ Ошибка проверки авторизации: {e}")
        return False

def run_db_status():
    """Проверяет статус БД на Railway"""
    print("\n🔍 Проверка статуса БД на Railway...")

    cmd = "railway ssh --project=b594ed19-0f61-46f0-94a8-a64c962c8fd8 --environment=141b8f58-c53e-4670-8e14-03a34285ef26 --service=eb58c45f-3990-474d-9d7c-1d970f1274b1 -- 'cd /app/game_app && python manage.py db_status'"

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )

        print("📊 СТАТУС БАЗЫ ДАННЫХ:")
        print("=" * 50)

        if result.returncode == 0:
            print("✅ Проверка успешна")
        else:
            print("❌ Ошибка проверки")

        if result.stdout:
            # Показываем только ключевую информацию
            lines = result.stdout.split('\n')
            for line in lines:
                if any(keyword in line.lower() for keyword in ['таблиц', 'миграций', 'суперпользовател', 'игроков', 'предметов']):
                    print(f"  {line}")

        if result.stderr:
            print("⚠️  Ошибки:")
            for line in result.stderr.split('\n')[:3]:
                if line.strip():
                    print(f"  {line}")

        return result.returncode == 0

    except subprocess.TimeoutExpired:
        print("⏰ Таймаут подключения к Railway")
        return False
    except Exception as e:
        print(f"💥 Ошибка: {e}")
        return False

def main():
    print("🚀 БЫСТРАЯ ПРОВЕРКА RAILWAY")
    print("=" * 40)

    # Проверки
    cli_ok = check_railway_cli()
    login_ok = check_railway_login() if cli_ok else False

    if cli_ok and login_ok:
        db_ok = run_db_status()
    else:
        db_ok = False
        print("\n❌ Пропускаем проверку БД - проблемы с Railway CLI")

    print("\n" + "=" * 40)
    print("📋 РЕЗУЛЬТАТ ПРОВЕРКИ:"    print(f"Railway CLI: {'✅' if cli_ok else '❌'}")
    print(f"Авторизация: {'✅' if login_ok else '❌'}")
    print(f"База данных: {'✅' if db_ok else '❌'}")

    if cli_ok and login_ok:
        print("\n💡 ГОТОВ К СБРОСУ БД!")
        print("Запустите: python railway_db_reset.py")
    else:
        print("\n⚠️  ИСПРАВЬТЕ ПРОБЛЕМЫ:")
        if not cli_ok:
            print("  - Установите Railway CLI")
        if not login_ok:
            print("  - Выполните: railway login")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Прервано пользователем")
    except Exception as e:
        print(f"\n💥 Критическая ошибка: {e}")
        sys.exit(1)
