from django.db import models
from django.utils import timezone


class Character(models.Model):
    """Модель персонажа игрока"""
    player = models.OneToOneField('accounts.Player', on_delete=models.CASCADE, related_name='character', verbose_name="Игрок", null=True, blank=True)
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
        from django.apps import apps
        Equipment = apps.get_model('characters', 'Equipment')

        # Базовые значения
        base_health = 100
        base_min_attack = 10
        base_max_attack = 15
        base_defense = 5

        # Применяем бонусы экипировки к первичным характеристикам
        effective_strength = self.strength
        effective_agility = self.agility
        effective_vitality = self.vitality

        # Бонусы от экипировки к первичным характеристикам
        equipment_strength_bonus = 0
        equipment_agility_bonus = 0
        equipment_vitality_bonus = 0

        # Бонусы от экипировки к вторичным характеристикам
        equipment_health_bonus = 0
        equipment_min_attack_bonus = 0
        equipment_max_attack_bonus = 0
        equipment_defense_bonus = 0
        equipment_crit_bonus = 0.0
        equipment_dodge_bonus = 0.0

        # Получаем бонусы от экипированных предметов
        try:
            for equip in Equipment.objects.filter(character=self):
                if equip.item:
                    # Бонусы к первичным характеристикам
                    equipment_strength_bonus += getattr(equip.item, 'strength_bonus', 0)
                    equipment_agility_bonus += getattr(equip.item, 'agility_bonus', 0)
                    equipment_vitality_bonus += getattr(equip.item, 'vitality_bonus', 0)

                    # Бонусы к вторичным характеристикам
                    equipment_health_bonus += getattr(equip.item, 'health_bonus', 0)
                    equipment_min_attack_bonus += getattr(equip.item, 'attack_bonus', 0)
                    equipment_max_attack_bonus += getattr(equip.item, 'attack_bonus', 0)
                    equipment_defense_bonus += getattr(equip.item, 'defense_bonus', 0)
                    equipment_crit_bonus += getattr(equip.item, 'crit_chance_bonus', 0)
                    equipment_dodge_bonus += getattr(equip.item, 'dodge_chance_bonus', 0)
        except Exception:
            # Если модель еще не доступна, пропускаем расчет
            pass

        # Применяем бонусы экипировки к первичным характеристикам
        effective_strength += equipment_strength_bonus
        effective_agility += equipment_agility_bonus
        effective_vitality += equipment_vitality_bonus

        # Модификаторы от навыков (используем эффективные значения)
        skill_health_bonus = (effective_vitality - 5) * 15  # +15 HP за каждый уровень живучести выше 5
        skill_min_attack_bonus = (effective_agility - 5) * 2  # +2 к мин атаке за ловкость
        skill_max_attack_bonus = (effective_strength - 5) * 3  # +3 к макс атаке за силу
        skill_defense_bonus = (effective_vitality - 5) * 2      # +2 к защите за живучесть
        skill_crit_bonus = (effective_strength - 5) * 1.5         # +1.5% крита за силу
        skill_dodge_bonus = (effective_agility - 5) * 1.0         # +1% уворота за ловкость

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


class Equipment(models.Model):
    """Экипировка персонажа"""

    # Слоты экипировки
    SLOTS = [
        ('weapon', 'Оружие'),
        ('torso', 'Торс'),
    ]

    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='equipment', verbose_name="Персонаж")
    slot = models.CharField(max_length=20, choices=SLOTS, unique=True, verbose_name="Слот")
    item = models.ForeignKey('items.Item', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Предмет")

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
