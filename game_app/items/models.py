from django.db import models
from django.utils import timezone


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
        ('gray', 'Серый'),
        ('green', 'Зеленый'),
        ('blue', 'Синий'),
        ('epic', 'Эпический'),
        ('legendary', 'Легендарный'),
    ]

    name = models.CharField(max_length=100, verbose_name="Название предмета")
    description = models.TextField(blank=True, verbose_name="Описание")

    item_type = models.CharField(max_length=20, choices=ITEM_TYPES, default='misc', verbose_name="Тип предмета")
    equipment_slot = models.CharField(max_length=20, choices=EQUIPMENT_SLOTS, default='none', verbose_name="Слот экипировки")
    rarity = models.CharField(max_length=20, choices=RARITIES, default='common', verbose_name="Редкость")

    # Свойства предметов
    # Бонусы к первичным характеристикам
    strength_bonus = models.IntegerField(default=0, verbose_name="Бонус к силе")
    agility_bonus = models.IntegerField(default=0, verbose_name="Бонус к ловкости")
    vitality_bonus = models.IntegerField(default=0, verbose_name="Бонус к живучести")

    # Бонусы к вторичным характеристикам
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

    player = models.OneToOneField('accounts.Player', on_delete=models.CASCADE, related_name='inventory', verbose_name="Игрок")
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
