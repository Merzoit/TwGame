# Используем официальный Python образ
FROM python:3.11-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Создаем директорию приложения
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Переходим в директорию Django проекта
WORKDIR /app/game_app

# Применяем миграции базы данных
RUN python manage.py migrate --noinput

# Создаем суперпользователя (если нужно)
RUN python manage.py create_superuser || echo "Superuser creation skipped"

# Создаем тестовые предметы
RUN python manage.py create_items || echo "Items creation skipped"

# Собираем статические файлы
RUN python manage.py collectstatic --noinput

# Возвращаемся в корневую директорию приложения
WORKDIR /app

# Создаем непривилегированного пользователя
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Открываем порт
EXPOSE 8000

# Команда запуска
CMD ["python", "game_app/manage.py", "runserver", "0.0.0.0:8000"]


