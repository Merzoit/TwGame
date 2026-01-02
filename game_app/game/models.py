from django.db import models
from django.utils import timezone

# Create your models here.

class Player(models.Model):
    """Модель игрока"""
    telegram_id = models.BigIntegerField(unique=True, verbose_name="Telegram ID")
    username = models.CharField(max_length=255, blank=True, null=True, verbose_name="Username")
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Имя")
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Фамилия")

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
