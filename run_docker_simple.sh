#!/bin/bash

echo "🐳 Быстрый запуск в Docker (SQLite)"
echo "==================================="

# Проверяем наличие Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен"
    exit 1
fi

echo "✅ Docker найден"

# Собираем образ
echo "🏗️  Сборка образа..."
docker build -t twgame:latest .

if [ $? -ne 0 ]; then
    echo "❌ Ошибка сборки"
    exit 1
fi

echo "✅ Образ собран"

# Запускаем контейнер
echo "🚀 Запуск контейнера..."
docker run -d \
    --name twgame_app \
    -p 8000:8000 \
    -e DEBUG=True \
    -e SECRET_KEY=django-insecure-dev-key \
    twgame:latest

if [ $? -ne 0 ]; then
    echo "❌ Ошибка запуска"
    exit 1
fi

echo "✅ Контейнер запущен"

# Ждем запуска
echo "⏳ Ожидание запуска..."
sleep 5

# Проверяем статус
echo "📊 Проверка статуса..."
if docker ps | grep -q twgame_app; then
    echo "✅ Приложение работает"
    echo "🌐 Доступно по адресу: http://localhost:8000"
    echo "🛑 Для остановки: docker stop twgame_app && docker rm twgame_app"
else
    echo "❌ Приложение не запустилось"
    echo "📝 Логи:"
    docker logs twgame_app
fi
