#!/usr/bin/env python3
"""
Проверка статуса базы данных на Railway
"""

import subprocess
import sys

def check_db_status():
    """Проверяет статус БД на Railway"""
    cmd = "railway ssh --project=b594ed19-0f61-46f0-94a8-a64c962c8fd8 --environment=141b8f58-c53e-4670-8e14-03a34285ef26 --service=eb58c45f-3990-474d-9d7c-1d970f1274b1 -- 'cd /app/game_app && python manage.py db_status'"

    print("🔍 Проверка статуса БД на Railway...")
    print(f"Команда: {cmd}")
    print()

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        print("📊 РЕЗУЛЬТАТ ПРОВЕРКИ:")
        print("=" * 50)

        if result.stdout:
            print("STDOUT:")
            print(result.stdout)

        if result.stderr:
            print("STDERR:")
            print(result.stderr)

        print("=" * 50)
        print(f"Exit code: {result.returncode}")

        if result.returncode == 0:
            print("✅ Проверка завершена успешно")
        else:
            print("❌ Ошибка при проверке статуса")

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Исключение: {e}")
        return False

if __name__ == '__main__':
    success = check_db_status()
    sys.exit(0 if success else 1)
