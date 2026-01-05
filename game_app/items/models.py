from django.db import models
from django.utils import timezone


class Item(models.Model):
    """Модель предмета в игре"""

    # Типы предметов
    ITEM_TYPES = [
        ('equipment', 'Экипировка'),
        ('craft', 'Крафт'),
        ('consumable', 'Расходный предмет'),
        ('resource', 'Ресурс'),
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

    # Тип предмета (экипировка или крафт)
    is_craftable = models.BooleanField(default=False, verbose_name="Крафтовый предмет")

    # Свойства предметов (только для экипировки)
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
        return self.equipment_slot != 'none' and not self.is_craftable

    @property
    def effective_strength_bonus(self):
        """Эффективный бонус к силе (только для экипировки)"""
        return self.strength_bonus if self.is_equippable else 0

    @property
    def effective_agility_bonus(self):
        """Эффективный бонус к ловкости (только для экипировки)"""
        return self.agility_bonus if self.is_equippable else 0

    @property
    def effective_vitality_bonus(self):
        """Эффективный бонус к живучести (только для экипировки)"""
        return self.vitality_bonus if self.is_equippable else 0

    @property
    def effective_attack_bonus(self):
        """Эффективный бонус к атаке (только для экипировки)"""
        return self.attack_bonus if self.is_equippable else 0

    @property
    def effective_defense_bonus(self):
        """Эффективный бонус к защите (только для экипировки)"""
        return self.defense_bonus if self.is_equippable else 0

    @property
    def effective_health_bonus(self):
        """Эффективный бонус к здоровью (только для экипировки)"""
        return self.health_bonus if self.is_equippable else 0

    @property
    def effective_crit_chance_bonus(self):
        """Эффективный бонус к шансу крита (только для экипировки)"""
        return self.crit_chance_bonus if self.is_equippable else 0.0

    @property
    def effective_dodge_chance_bonus(self):
        """Эффективный бонус к шансу уворота (только для экипировки)"""
        return self.dodge_chance_bonus if self.is_equippable else 0.0


class EquipmentItems(models.Model):
    """Предметы, которые можно экипировать"""

    # Слоты экипировки
    EQUIPMENT_SLOTS = [
        ('weapon', 'оружие'),
        ('head', 'голова'),
        ('body', 'тело/торс'),
        ('legs', 'ноги'),
        ('hands', 'руки'),
        ('feet', 'обувь'),
        ('amulet', 'амулет'),
        ('ring', 'кольцо'),
    ]

    # Редкость предметов
    RARITIES = [
        ('common', 'обычный (серый)'),
        ('uncommon', 'необычный (зеленый)'),
        ('rare', 'редкий (синий)'),
        ('epic', 'эпический (фиолетовый)'),
        ('legendary', 'легендарный (оранжевый)'),
    ]

    item = models.OneToOneField(Item, on_delete=models.CASCADE, related_name='equipment_info', verbose_name="Предмет")
    equipment_slot = models.CharField(max_length=20, choices=EQUIPMENT_SLOTS, verbose_name="Слот для экипировки")
    rarity = models.CharField(max_length=20, choices=RARITIES, default='common', verbose_name="Редкость предмета")

    # Бонусы к характеристикам (по всем статам)
    strength_bonus = models.IntegerField(default=0, verbose_name="Бонус к силе")
    agility_bonus = models.IntegerField(default=0, verbose_name="Бонус к ловкости")
    vitality_bonus = models.IntegerField(default=0, verbose_name="Бонус к живучести")
    attack_bonus = models.IntegerField(default=0, verbose_name="Бонус к атаке")
    defense_bonus = models.IntegerField(default=0, verbose_name="Бонус к защите")
    health_bonus = models.IntegerField(default=0, verbose_name="Бонус к здоровью")
    crit_chance_bonus = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="Бонус к шансу крита (%)")
    dodge_chance_bonus = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="Бонус к шансу уворота (%)")

    level_requirement = models.IntegerField(default=1, verbose_name="Требуемый уровень")

    class Meta:
        verbose_name = "Предмет экипировки"
        verbose_name_plural = "Предметы экипировки"

    def __str__(self):
        return f"{self.item.name} ({self.get_rarity_display()})"


class CraftItems(models.Model):
    """Предметы для крафта и ресурсы"""
    item = models.OneToOneField(Item, on_delete=models.CASCADE, related_name='craft_info', verbose_name="Предмет")
    stack_size = models.IntegerField(default=1, verbose_name="Максимальный размер стопки")
    is_craftable = models.BooleanField(default=False, verbose_name="Можно ли использовать в крафте")

    class Meta:
        verbose_name = "Предмет крафта"
        verbose_name_plural = "Предметы крафта"

    def __str__(self):
        return f"{self.item.name} (стопка: {self.stack_size})"


class Inventory(models.Model):
    """Хранение предметов игрока"""

    # Слоты экипировки для инвентаря
    EQUIPMENT_SLOTS = [
        ('weapon', 'оружие'),
        ('head', 'голова'),
        ('body', 'тело/торс'),
        ('legs', 'ноги'),
        ('hands', 'руки'),
        ('feet', 'обувь'),
        ('amulet', 'амулет'),
        ('ring', 'кольцо'),
        ('none', 'не экипирован'),
    ]

    player = models.ForeignKey('accounts.Player', on_delete=models.CASCADE, related_name='inventory', verbose_name="Игрок")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Предмет")
    quantity = models.IntegerField(default=1, verbose_name="Количество предметов")
    is_equipped = models.BooleanField(default=False, verbose_name="Экипирован ли предмет")
    equipped_slot = models.CharField(max_length=20, choices=EQUIPMENT_SLOTS, default='none', verbose_name="В каком слоте экипирован")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Инвентарь"
        verbose_name_plural = "Инвентари"
        unique_together = ['player', 'item']

    def __str__(self):
        equipped = " (экипирован)" if self.is_equipped else ""
        return f"{self.player} - {self.item.name} x{self.quantity}{equipped}"


class PlayerEquipment(models.Model):
    """Быстрый доступ к экипированным предметам"""

    # Слоты экипировки
    EQUIPMENT_SLOTS = [
        ('weapon', 'оружие'),
        ('head', 'голова'),
        ('body', 'тело/торс'),
        ('legs', 'ноги'),
        ('hands', 'руки'),
        ('feet', 'обувь'),
        ('amulet', 'амулет'),
        ('ring', 'кольцо'),
    ]

    player = models.OneToOneField('accounts.Player', on_delete=models.CASCADE, related_name='equipment', verbose_name="Игрок")

    # Ссылки на предметы в слотах
    weapon_slot = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True, related_name='weapon_equipped', verbose_name="Оружие")
    head_slot = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True, related_name='head_equipped', verbose_name="Голова")
    body_slot = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True, related_name='body_equipped', verbose_name="Тело")
    legs_slot = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True, related_name='legs_equipped', verbose_name="Ноги")
    hands_slot = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True, related_name='hands_equipped', verbose_name="Руки")
    feet_slot = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True, related_name='feet_equipped', verbose_name="Обувь")
    amulet_slot = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True, related_name='amulet_equipped', verbose_name="Амулет")
    ring_slot = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True, related_name='ring_equipped', verbose_name="Кольцо")

    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Экипировка игрока"
        verbose_name_plural = "Экипировка игроков"

    def __str__(self):
        return f"Экипировка {self.player}"

    def get_equipped_items(self):
        """Возвращает словарь экипированных предметов"""
        return {
            'weapon': self.weapon_slot,
            'head': self.head_slot,
            'body': self.body_slot,
            'legs': self.legs_slot,
            'hands': self.hands_slot,
            'feet': self.feet_slot,
            'amulet': self.amulet_slot,
            'ring': self.ring_slot,
        }
