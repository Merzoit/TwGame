# TwGame

Игра в Telegram с веб-интерфейсом на Django и современным игровым стилем на JavaScript.

## Описание проекта

TwGame - это комплексная игровая платформа, состоящая из:
- Telegram бота для входа в игру
- Веб-интерфейса на Django с игровыми механиками
- Современного UI на JavaScript

## Структура проекта

```
TwGame/
├── telegram_bot/          # Telegram бот
│   ├── main.py           # Основной скрипт бота
│   ├── requirements.txt  # Зависимости
│   └── README.md         # Документация бота
├── images/               # Игровые изображения
└── README.md             # Этот файл
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

- **Backend**: Django (планируется)
- **Frontend**: JavaScript, HTML5, CSS3
- **Bot**: Python, python-telegram-bot
- **Database**: PostgreSQL (планируется)

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd TwGame
```

2. Запустите бота:
```bash
cd telegram_bot
pip install -r requirements.txt
python main.py
```

## Лицензия

MIT License
