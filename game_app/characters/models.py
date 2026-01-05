from django.db import models
from django.utils import timezone


class Character(models.Model):
    """Игровой персонаж пользователя (1:1 с игроком)"""
    player = models.OneToOneField('accounts.Player', on_delete=models.CASCADE, related_name='character', verbose_name="Игрок")
    name = models.CharField(max_length=50, verbose_name="Имя персонажа")
    experience = models.IntegerField(default=0, verbose_name="Текущий опыт")
    level = models.IntegerField(default=1, verbose_name="Текущий уровень")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Персонаж"
        verbose_name_plural = "Персонажи"

    def __str__(self):
        return f"{self.name} - {self.player}"

    def __str__(self):
        return f"{self.name} - Уровень {self.level}"


class CharacterStats(models.Model):
    """Игровые характеристики персонажа (1:1 с персонажем)"""
    character = models.OneToOneField(Character, on_delete=models.CASCADE, related_name='stats', verbose_name="Персонаж")
    health = models.IntegerField(default=100, verbose_name="Текущее здоровье")
    max_health = models.IntegerField(default=100, verbose_name="Максимальное здоровье")
    agility = models.IntegerField(default=5, verbose_name="Ловкость")
    strength = models.IntegerField(default=5, verbose_name="Сила")
    vitality = models.IntegerField(default=5, verbose_name="Живучесть")
    min_attack = models.IntegerField(default=10, verbose_name="Минимальная атака")
    max_attack = models.IntegerField(default=15, verbose_name="Максимальная атака")
    critical_chance = models.DecimalField(max_digits=5, decimal_places=2, default=5.00, verbose_name="Шанс критического удара (%)")
    dodge_chance = models.DecimalField(max_digits=5, decimal_places=2, default=5.00, verbose_name="Шанс уворота (%)")
    defense = models.IntegerField(default=5, verbose_name="Защита")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Характеристики персонажа"
        verbose_name_plural = "Характеристики персонажей"

    def __str__(self):
        return f"Статистика {self.character.name}"


# Модель Equipment оставлена для обратной совместимости
# Основная экипировка теперь в PlayerEquipment в items/models.py
