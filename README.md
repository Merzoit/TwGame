# TwGame

Игра в Telegram с веб-интерфейсом на Django и современным игровым стилем на JavaScript.

## 🚀 Демо

- **Telegram бот**: [@MerzoitCodeBot](https://t.me/MerzoitCodeBot)
- **Веб-приложение**: [Railway App](https://twgame-production.up.railway.app/) (скоро будет доступно)

## Описание проекта

TwGame - это комплексная игровая платформа, состоящая из:
- Telegram бота для входа в игру
- Веб-интерфейса на Django с игровыми механиками
- Современного UI с glass-morphism дизайном

## Структура проекта

```
TwGame/
├── game_app/             # Django веб-приложение
│   ├── twgame/          # Настройки проекта
│   ├── game/            # Игровое приложение
│   ├── requirements.txt # Зависимости Django
│   └── README.md        # Документация Django
├── telegram_bot/        # Telegram бот
│   ├── main.py          # Основной скрипт бота
│   ├── requirements.txt # Зависимости бота
│   └── README.md        # Документация бота
├── images/              # Игровые изображения
├── requirements.txt     # Общие зависимости
├── railway.json         # Конфигурация Railway
├── start.sh            # Скрипт запуска
└── README.md           # Этот файл
```

## Telegram Bot

Бот доступен по адресу: [@MerzoitCodeBot](https://t.me/MerzoitCodeBot)

### Запуск бота

```bash
cd telegram_bot
pip install -r requirements.txt
python main.py
```

## Разработка

Проект находится в активной разработке. Планируется реализация:
- Магазин предметов
- Инвентарь игрока
- Система профилей
- Квестовая система
- Крафт предметов
- И другие игровые механики

## Технологии

- **Backend**: Django 5.1, Django REST Framework
- **Frontend**: JavaScript, HTML5, CSS3 (Glass-morphism дизайн)
- **Bot**: Python, python-telegram-bot
- **Database**: PostgreSQL (Railway) / SQLite (development)
- **Deployment**: Railway, Gunicorn, WhiteNoise

## 🚀 Деплой на Railway

Проект автоматически развертывается на Railway при пуше в main ветку.

### Настройка переменных окружения в Railway:

В панели управления Railway добавьте следующие переменные:

```bash
DEBUG=False
SECRET_KEY=ваш-секретный-ключ-django
ALLOWED_HOSTS=your-railway-app-url.up.railway.app
DATABASE_URL=postgresql://... (Railway предоставит автоматически)
TELEGRAM_BOT_TOKEN=8567389465:AAGf6VKykyl6REaiDz-Vqu2QTacQbvURS7k
```

### Локальная разработка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd TwGame
```

2. **Запуск веб-приложения:**
```bash
cd game_app
pip install -r ../requirements.txt
python manage.py migrate
python manage.py runserver
```

3. **Запуск Telegram бота** (в отдельном терминале):
```bash
cd telegram_bot
pip install -r requirements.txt
python main.py
```

### URLs после запуска:
- **Веб-приложение**: http://127.0.0.1:8000
- **Telegram бот**: [@MerzoitCodeBot](https://t.me/MerzoitCodeBot)

## Лицензия

MIT License
