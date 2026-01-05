from django.db import models
from django.utils import timezone


class Player(models.Model):
    """Модель игрока"""
    telegram_id = models.BigIntegerField(unique=True, verbose_name="Telegram ID")
    telegram_username = models.CharField(max_length=255, blank=True, null=True, verbose_name="Имя пользователя Telegram")
    twitch_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="Twitch ID")
    twitch_username = models.CharField(max_length=255, blank=True, null=True, verbose_name="Имя пользователя Twitch")
    twitch_connected = models.BooleanField(default=False, verbose_name="Статус подключения к Twitch")
    twitch_access_token = models.TextField(blank=True, null=True, verbose_name="Токен доступа Twitch")
    twitch_refresh_token = models.TextField(blank=True, null=True, verbose_name="Токен обновления Twitch")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата регистрации")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего обновления")
    last_login = models.DateTimeField(blank=True, null=True, verbose_name="Дата последнего входа")

    class Meta:
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username or self.first_name or 'User'} (ID: {self.telegram_id})"


class PlayerStats(models.Model):
    """Статистические данные игрока (отношение 1:1)"""
    player = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='stats', verbose_name="Игрок")
    total_matches = models.IntegerField(default=0, verbose_name="Общее количество матчей")
    wins = models.IntegerField(default=0, verbose_name="Количество побед")
    gold = models.IntegerField(default=0, verbose_name="Количество золота")
    diamonds = models.IntegerField(default=0, verbose_name="Количество алмазов")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Статистика игрока"
        verbose_name_plural = "Статистика игроков"

    def __str__(self):
        return f"Статистика {self.player}"

    @property
    def losses(self):
        """Количество поражений"""
        return self.total_matches - self.wins

    @property
    def win_rate(self):
        """Процент побед"""
        if self.total_matches == 0:
            return 0
        return round((self.wins / self.total_matches) * 100, 1)
