# TwGame Django Web App

Веб-приложение для игры TwGame, интегрированное с Telegram ботом.

## Установка и запуск

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Выполните миграции базы данных:
```bash
python manage.py migrate
```

3. Создайте суперпользователя (опционально):
```bash
python manage.py createsuperuser
```

4. Запустите сервер разработки:
```bash
python manage.py runserver
```

Приложение будет доступно по адресу: http://127.0.0.1:8000

## Структура проекта

- `twgame/` - настройки Django проекта
- `game/` - основное приложение игры
- `templates/game/` - HTML шаблоны
- `static/` - статические файлы (CSS, JS, изображения)

## API endpoints

- `GET /` - главная страница игры
- `GET /api/status/` - статус API
- `POST /api/telegram/webhook/` - вебхук для Telegram бота

## Разработка

### Добавление нового функционала

1. Создайте новое представление в `game/views.py`
2. Добавьте URL в `game/urls.py`
3. Создайте шаблон в `game/templates/game/`
4. Добавьте стили и JavaScript по необходимости

### Модели данных

Пока модели данных не определены. В будущем будут добавлены модели для:
- Игроков (Players)
- Инвентаря (Inventory)
- Квестов (Quests)
- Предметов (Items)

## Деплой

Для продакшена рекомендуется использовать:
- PostgreSQL вместо SQLite
- Nginx + Gunicorn
- Docker для контейнеризации

## Лицензия

MIT
