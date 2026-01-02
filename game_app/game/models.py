from django.db import models
from django.utils import timezone

# Create your models here.

class Player(models.Model):
    """Модель игрока"""
    telegram_id = models.BigIntegerField(unique=True, verbose_name="Telegram ID")
    username = models.CharField(max_length=255, blank=True, null=True, verbose_name="Username")
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Имя")
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Фамилия")

    # Twitch интеграция
    twitch_username = models.CharField(max_length=255, blank=True, null=True, verbose_name="Twitch username")
    twitch_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="Twitch ID")
    twitch_connected = models.BooleanField(default=False, verbose_name="Twitch подключен")

    # Системные поля
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username or self.first_name or 'User'} (ID: {self.telegram_id})"

class PlayerProfile(models.Model):
    """Профиль игрока с игровыми данными"""
    player = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='profile', verbose_name="Игрок")

    # Основные характеристики
    level = models.IntegerField(default=1, verbose_name="Уровень")
    experience = models.IntegerField(default=0, verbose_name="Опыт")
    gold = models.IntegerField(default=100, verbose_name="Золото")

    # Статистика
    total_games = models.IntegerField(default=0, verbose_name="Всего игр")
    wins = models.IntegerField(default=0, verbose_name="Побед")
    losses = models.IntegerField(default=0, verbose_name="Поражений")

    # Дата и время
    last_login = models.DateTimeField(default=timezone.now, verbose_name="Последний вход")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания профиля")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Профиль игрока"
        verbose_name_plural = "Профили игроков"
        ordering = ['-level', '-experience']

    def __str__(self):
        return f"Профиль {self.player} - Уровень {self.level}"

    @property
    def win_rate(self):
        """Процент побед"""
        if self.total_games == 0:
            return 0
        return round((self.wins / self.total_games) * 100, 1)

    def add_experience(self, amount):
        """Добавить опыт и проверить повышение уровня"""
        self.experience += amount
        # Простая система уровней: каждые 100 опыта = 1 уровень
        new_level = (self.experience // 100) + 1
        if new_level > self.level:
            old_level = self.level
            self.level = new_level
            return new_level - old_level  # Возвращаем количество уровней, на которое поднялись
        return 0


class Character(models.Model):
    """Модель персонажа игрока"""
    CLASS_CHOICES = [
        ('warrior', 'Воин'),
        ('mage', 'Маг'),
        ('assassin', 'Ассасин'),
    ]

    player = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='character', verbose_name="Игрок", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name="Имя персонажа")
    class_type = models.CharField(max_length=20, choices=CLASS_CHOICES, verbose_name="Класс")

    # Базовые характеристики
    level = models.IntegerField(default=1, verbose_name="Уровень")
    experience = models.IntegerField(default=0, verbose_name="Опыт")

    # Здоровье и мана
    max_health = models.IntegerField(default=100, verbose_name="Максимальное здоровье")
    current_health = models.IntegerField(default=100, verbose_name="Текущее здоровье")
    max_mana = models.IntegerField(default=50, verbose_name="Максимальная мана")
    current_mana = models.IntegerField(default=50, verbose_name="Текущая мана")

    # Бойевые характеристики (базовые значения зависят от класса)
    base_attack = models.IntegerField(default=10, verbose_name="Базовая атака")
    base_defense = models.IntegerField(default=5, verbose_name="Базовая защита")
    base_speed = models.IntegerField(default=10, verbose_name="Базовая скорость")

    # Дата создания и обновления
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Персонаж"
        verbose_name_plural = "Персонажи"

    def __str__(self):
        return f"{self.name} ({self.get_class_type_display()}) - {self.player}"

    @property
    def class_display_name(self):
        """Отображаемое имя класса с эмодзи"""
        class_emojis = {
            'warrior': '⚔️ Воин',
            'mage': '🔮 Маг',
            'assassin': '🗡️ Ассасин'
        }
        return class_emojis.get(self.class_type, self.get_class_type_display())

    @property
    def attack_power(self):
        """Общая сила атаки (базовая + модификаторы)"""
        return self.base_attack * (1 + (self.level - 1) * 0.1)

    @property
    def defense(self):
        """Общая защита (базовая + модификаторы)"""
        return self.base_defense * (1 + (self.level - 1) * 0.1)

    @property
    def speed(self):
        """Общая скорость (базовая + модификаторы)"""
        return self.base_speed * (1 + (self.level - 1) * 0.05)

    def save(self, *args, **kwargs):
        """Переопределяем save для установки базовых характеристик при создании"""
        if not self.pk:  # Если объект только создается
            self.set_base_stats()
        super().save(*args, **kwargs)

    def set_base_stats(self):
        """Устанавливаем базовые характеристики в зависимости от класса"""
        class_stats = {
            'warrior': {
                'max_health': 150,
                'max_mana': 30,
                'base_attack': 15,
                'base_defense': 12,
                'base_speed': 8
            },
            'mage': {
                'max_health': 80,
                'max_mana': 120,
                'base_attack': 20,
                'base_defense': 3,
                'base_speed': 10
            },
            'assassin': {
                'max_health': 100,
                'max_mana': 60,
                'base_attack': 18,
                'base_defense': 5,
                'base_speed': 15
            }
        }

        stats = class_stats.get(self.class_type, class_stats['warrior'])
        for attr, value in stats.items():
            setattr(self, attr, value)

        # Устанавливаем текущее здоровье и ману равными максимальным
        self.current_health = self.max_health
        self.current_mana = self.max_mana
