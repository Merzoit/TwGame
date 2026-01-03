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
    twitch_access_token = models.TextField(blank=True, null=True, verbose_name="Twitch access token")
    twitch_refresh_token = models.TextField(blank=True, null=True, verbose_name="Twitch refresh token")
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
    player = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='character', verbose_name="Игрок", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name="Имя персонажа")

    # Навыки персонажа (влияют на характеристики)
    strength = models.IntegerField(default=5, verbose_name="Сила")  # Максимальная атака, сила крита
    agility = models.IntegerField(default=5, verbose_name="Ловкость")  # Минимальная атака, уворот
    vitality = models.IntegerField(default=5, verbose_name="Живучесть")  # HP, защита

    # Свободные очки навыков
    free_skill_points = models.IntegerField(default=5, verbose_name="Свободные очки навыков")

    # Базовые характеристики
    level = models.IntegerField(default=1, verbose_name="Уровень")
    experience = models.IntegerField(default=0, verbose_name="Опыт")

    # Здоровье и мана
    max_health = models.IntegerField(default=100, verbose_name="Максимальное здоровье")
    current_health = models.IntegerField(default=100, verbose_name="Текущее здоровье")

    # Бойевые характеристики (базовые значения зависят от класса)
    min_attack = models.IntegerField(default=10, verbose_name="Минимальная атака")
    max_attack = models.IntegerField(default=15, verbose_name="Максимальная атака")
    defense = models.IntegerField(default=5, verbose_name="Защита")
    crit_chance = models.FloatField(default=5.0, verbose_name="Шанс крита (%)")
    dodge_chance = models.FloatField(default=5.0, verbose_name="Шанс уворота (%)")

    # Дата создания и обновления
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Персонаж"
        verbose_name_plural = "Персонажи"

    def __str__(self):
        return f"{self.name} - {self.player}"

    def calculate_stats(self):
        """Расчет характеристик на основе навыков и экипировки"""
        # Базовые значения
        base_health = 100
        base_min_attack = 10
        base_max_attack = 15
        base_defense = 5

        # Модификаторы от навыков
        skill_health_bonus = (self.vitality - 5) * 15  # +15 HP за каждый уровень живучести выше 5
        skill_min_attack_bonus = (self.agility - 5) * 2  # +2 к мин атаке за ловкость
        skill_max_attack_bonus = (self.strength - 5) * 3  # +3 к макс атаке за силу
        skill_defense_bonus = (self.vitality - 5) * 2      # +2 к защите за живучесть
        skill_crit_bonus = (self.strength - 5) * 1.5         # +1.5% крита за силу
        skill_dodge_bonus = (self.agility - 5) * 1.0         # +1% уворота за ловкость

        # Бонусы от экипировки
        equipment_health_bonus = 0
        equipment_min_attack_bonus = 0
        equipment_max_attack_bonus = 0
        equipment_defense_bonus = 0
        equipment_crit_bonus = 0.0
        equipment_dodge_bonus = 0.0

        # Получаем бонусы от экипированных предметов
        for equip in self.equipment.all():
            if equip.item:
                equipment_health_bonus += equip.item.health_bonus
                equipment_min_attack_bonus += equip.item.attack_bonus
                equipment_max_attack_bonus += equip.item.attack_bonus
                equipment_defense_bonus += equip.item.defense_bonus
                equipment_crit_bonus += equip.item.crit_chance_bonus
                equipment_dodge_bonus += equip.item.dodge_chance_bonus

        # Итоговые характеристики
        self.max_health = base_health + skill_health_bonus + equipment_health_bonus
        self.min_attack = base_min_attack + skill_min_attack_bonus + equipment_min_attack_bonus
        self.max_attack = base_max_attack + skill_max_attack_bonus + equipment_max_attack_bonus
        self.defense = base_defense + skill_defense_bonus + equipment_defense_bonus
        self.crit_chance = 5.0 + skill_crit_bonus + equipment_crit_bonus
        self.dodge_chance = 5.0 + skill_dodge_bonus + equipment_dodge_bonus

        # Устанавливаем текущие значения равными максимальным
        self.current_health = self.max_health

    def save(self, *args, **kwargs):
        """Переопределяем save для расчета характеристик"""
        # Всегда пересчитываем характеристики при сохранении
        self.calculate_stats()
        super().save(*args, **kwargs)


class Item(models.Model):
    """Модель предмета в игре"""

    # Типы предметов
    ITEM_TYPES = [
        ('weapon', 'Оружие'),
        ('armor', 'Броня'),
        ('consumable', 'Расходуемое'),
        ('resource', 'Ресурс'),
        ('misc', 'Разное'),
    ]

    # Слоты экипировки
    EQUIPMENT_SLOTS = [
        ('weapon', 'Оружие'),
        ('torso', 'Торс'),
        ('head', 'Голова'),
        ('hands', 'Руки'),
        ('legs', 'Ноги'),
        ('feet', 'Ступни'),
        ('accessory', 'Аксессуар'),
        ('none', 'Не экипируется'),
    ]

    # Редкость предметов
    RARITIES = [
        ('common', 'Обычный'),
        ('uncommon', 'Необычный'),
        ('rare', 'Редкий'),
        ('epic', 'Эпический'),
        ('legendary', 'Легендарный'),
    ]

    name = models.CharField(max_length=100, verbose_name="Название предмета")
    description = models.TextField(blank=True, verbose_name="Описание")

    item_type = models.CharField(max_length=20, choices=ITEM_TYPES, default='misc', verbose_name="Тип предмета")
    equipment_slot = models.CharField(max_length=20, choices=EQUIPMENT_SLOTS, default='none', verbose_name="Слот экипировки")
    rarity = models.CharField(max_length=20, choices=RARITIES, default='common', verbose_name="Редкость")

    # Свойства предметов
    attack_bonus = models.IntegerField(default=0, verbose_name="Бонус к атаке")
    defense_bonus = models.IntegerField(default=0, verbose_name="Бонус к защите")
    health_bonus = models.IntegerField(default=0, verbose_name="Бонус к здоровью")
    crit_chance_bonus = models.FloatField(default=0.0, verbose_name="Бонус к шансу крита (%)")
    dodge_chance_bonus = models.FloatField(default=0.0, verbose_name="Бонус к шансу уворота (%)")

    # Цена и свойства
    value = models.IntegerField(default=0, verbose_name="Цена предмета")
    stackable = models.BooleanField(default=False, verbose_name="Можно складывать")
    max_stack = models.IntegerField(default=1, verbose_name="Максимум в стопке")

    # Системные поля
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"
        ordering = ['name']

    def __str__(self):
        return f"{self.get_rarity_display()} {self.name}"

    @property
    def is_equippable(self):
        """Проверяет, можно ли экипировать предмет"""
        return self.equipment_slot != 'none'


class Inventory(models.Model):
    """Инвентарь игрока"""

    player = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='inventory', verbose_name="Игрок")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Предмет")
    quantity = models.IntegerField(default=1, verbose_name="Количество")

    # Дата получения
    obtained_at = models.DateTimeField(default=timezone.now, verbose_name="Дата получения")

    class Meta:
        verbose_name = "Инвентарь"
        verbose_name_plural = "Инвентари"
        unique_together = ['player', 'item']  # Один предмет - одно место в инвентаре
        ordering = ['-obtained_at']

    def __str__(self):
        return f"{self.player} - {self.item.name} x{self.quantity}"

    @property
    def total_value(self):
        """Общая стоимость предметов"""
        return self.item.value * self.quantity


class Equipment(models.Model):
    """Экипировка персонажа"""

    # Слоты экипировки
    SLOTS = [
        ('weapon', 'Оружие'),
        ('torso', 'Торс'),
    ]

    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='equipment', verbose_name="Персонаж")
    slot = models.CharField(max_length=20, choices=SLOTS, unique=True, verbose_name="Слот")
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Предмет")

    # Дата экипировки
    equipped_at = models.DateTimeField(default=timezone.now, verbose_name="Дата экипировки")

    class Meta:
        verbose_name = "Экипировка"
        verbose_name_plural = "Экипировки"
        unique_together = ['character', 'slot']

    def __str__(self):
        item_name = self.item.name if self.item else "Пусто"
        return f"{self.character.name} - {self.get_slot_display()}: {item_name}"

    def save(self, *args, **kwargs):
        """При экипировке пересчитываем характеристики персонажа"""
        super().save(*args, **kwargs)
        self.character.save()  # Пересчет характеристик

    def delete(self, *args, **kwargs):
        """При снятии экипировки пересчитываем характеристики"""
        super().delete(*args, **kwargs)
        self.character.save()  # Пересчет характеристик
