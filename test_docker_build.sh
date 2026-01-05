#!/bin/bash

echo "🐳 Тестирование Docker сборки"
echo "============================"

# Проверяем наличие Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен"
    exit 1
fi

echo "✅ Docker найден"

# Останавливаем и удаляем старые контейнеры
echo "🧹 Очистка старых контейнеров..."
docker-compose down -v 2>/dev/null || true
docker system prune -f 2>/dev/null || true

# Собираем образ
echo "🏗️  Сборка Docker образа..."
if docker-compose build --no-cache; then
    echo "✅ Сборка прошла успешно"
else
    echo "❌ Ошибка сборки"
    exit 1
fi

# Запускаем сервисы
echo "🚀 Запуск контейнеров..."
if docker-compose up -d; then
    echo "✅ Контейнеры запущены"
else
    echo "❌ Ошибка запуска"
    exit 1
fi

# Ждем запуска
echo "⏳ Ожидание запуска сервисов..."
sleep 10

# Проверяем статус
echo "📊 Проверка статуса..."
if docker-compose ps | grep -q "Up"; then
    echo "✅ Сервисы работают"

    # Проверяем логи веб-сервера
    echo "📝 Логи веб-сервера:"
    docker-compose logs web | tail -20

    echo ""
    echo "🌐 Приложение доступно по адресу: http://localhost:8000"
    echo "🛑 Для остановки выполните: docker-compose down"

else
    echo "❌ Сервисы не запустились"
    echo "📝 Логи:"
    docker-compose logs
    exit 1
fi

echo ""
echo "🎉 Docker тестирование завершено успешно!"
