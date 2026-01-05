# TwGame - Telegram RPG Game

Современная Telegram-игра в стиле RPG с системой персонажей, предметов, инвентаря и экипировки.

## 🚀 Особенности

- **Telegram Web App** - игра запускается прямо в Telegram
- **Система персонажей** - навыки, уровни, характеристики
- **Инвентарь и экипировка** - предметы с бонусами
- **Админ панель** - удобное управление базой данных
- **REST API** - для интеграций и расширений
- **Современный UI** - responsive дизайн с анимациями

## 📁 Архитектура проекта

Проект разделен на логические приложения Django для лучшей организации и масштабируемости:

### 🏗️ Структура приложений

```
twgame/
├── core/                    # Базовые модели и утилиты
│   ├── models.py           # BaseModel, GameSettings, GameLog
│   └── ...
├── accounts/               # Управление пользователями
│   ├── models.py           # Player, PlayerProfile
│   ├── services.py         # PlayerService
│   └── ...
├── characters/             # Система персонажей
│   ├── models.py           # Character, Equipment
│   └── ...
├── items/                  # Предметы и инвентарь
│   ├── models.py           # Item, Inventory
│   └── ...
├── game/                   # Основная игровая логика
│   ├── views.py            # Главная игра, создание персонажа
│   └── templates/
├── admin_panel/            # Административная панель
│   ├── views.py            # Управление данными
│   └── templates/
├── api/                    # REST API
│   ├── views.py            # API endpoints
│   ├── serializers.py      # Сериализаторы
│   └── urls.py
├── telegram_bot/           # Интеграция с Telegram
├── twitch_integration/     # Интеграция с Twitch
└── twgame/                 # Настройки проекта
    ├── settings.py
    └── urls.py
```

## 🔧 Установка и запуск

### Требования
- Python 3.11+
- Django 5.1+
- PostgreSQL/MySQL (рекомендуется для продакшена)

### Локальная разработка

1. **Клонировать репозиторий:**
```bash
git clone <repository-url>
cd twgame
```

2. **Создать виртуальное окружение:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

3. **Установить зависимости:**
```bash
pip install -r requirements.txt
```

4. **Настроить базу данных:**
```bash
python manage.py migrate
```

5. **Создать суперпользователя:**
```bash
python manage.py createsuperuser
```

6. **Запустить сервер разработки:**
```bash
python manage.py runserver
```

## 🎮 Использование

### Веб-интерфейс
- **Главная игра:** `/`
- **Админ панель:** `/db-admin/`
- **Django Admin:** `/admin/`

### Telegram Bot
Интегрируется с Telegram Web Apps для запуска игры прямо в мессенджере.

## 📊 Админ панель

Мощная административная панель для управления всеми данными игры:

### Разделы админки:
- **🏠 Дашборд** - статистика и быстрые действия
- **👥 Игроки** - управление учетными записями
- **⚔️ Персонажи** - управление персонажами
- **📦 Предметы** - создание и редактирование предметов
- **🎒 Инвентарь** - просмотр инвентарей игроков
- **🛡️ Экипировка** - управление экипировкой

### Создание предметов
В админке можно создавать предметы со всеми характеристиками:
- Бонусы к силе, ловкости, живучести
- Боевые параметры (атака, защита, крит)
- Редкость и тип предмета
- Цена и свойства

## 🔌 API

REST API для интеграций:

### Основные endpoints:
```
GET  /api/players/         # Список игроков
GET  /api/characters/      # Список персонажей
GET  /api/items/           # Список предметов
POST /api/game/equip-item/ # Экипировка предмета
POST /api/game/unequip-item/ # Снятие предмета
```

### Аутентификация
API использует токены или сессии для аутентификации.

## 🗃️ Модели данных

### Player (accounts)
- telegram_id: уникальный ID в Telegram
- username, first_name, last_name: данные пользователя
- Twitch интеграция: username, access_token и т.д.

### Character (characters)
- player: ссылка на игрока
- name: имя персонажа
- strength, agility, vitality: основные навыки
- Бойевые характеристики (атака, защита, крит)

### Item (items)
- name, description: описание предмета
- item_type, rarity: тип и редкость
- Бонусы характеристик (strength_bonus, attack_bonus и т.д.)
- equipment_slot: слот экипировки

### Equipment (characters)
- character: персонаж
- item: предмет
- slot: слот экипировки (weapon, torso)

## 🚀 Развертывание

### Railway (рекомендуется)
Проект настроен для развертывания на Railway:

1. Создать аккаунт на [Railway.app](https://railway.app)
2. Подключить GitHub репозиторий
3. Настроить переменные окружения
4. Деплой

### Переменные окружения
```env
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://...
ALLOWED_HOSTS=your-domain.com
TELEGRAM_BOT_TOKEN=your-bot-token
TWITCH_CLIENT_ID=your-twitch-client-id
TWITCH_CLIENT_SECRET=your-twitch-client-secret
```

## 🔧 Разработка

### Добавление новых предметов
1. Перейти в админку `/db-admin/`
2. Раздел "Предметы" → "Создать предмет"
3. Заполнить все поля и сохранить

### Расширение системы
- **Новые предметы:** добавить в `items/models.py`
- **Новые навыки:** обновить `characters/models.py`
- **Новые API:** добавить в `api/views.py`
- **Новый UI:** добавить в соответствующие templates

## 📈 Производительность

### Оптимизации:
- **select_related/prefetch_related** для связанных запросов
- **Индексы** на часто используемых полях
- **Кэширование** для статических данных
- **Пагинация** для больших списков

### Мониторинг:
- **GameLog** модель для логирования событий
- **Django Debug Toolbar** для локальной разработки
- **Sentry** для отслеживания ошибок

## 🤝 Вклад в проект

1. Fork репозиторий
2. Создать feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit изменения (`git commit -m 'Add some AmazingFeature'`)
4. Push в branch (`git push origin feature/AmazingFeature`)
5. Создать Pull Request

## 📝 Лицензия

Этот проект распространяется под лицензией MIT.

## 📞 Контакты

- **Email:** admin@twgame.com
- **Telegram:** @twgame_bot
- **GitHub:** [репозиторий]

---

**TwGame** - современная Telegram-игра с мощной административной панелью и REST API! 🚀🎮