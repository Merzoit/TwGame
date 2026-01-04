from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """Базовая модель с общими полями"""

    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        abstract = True


class GameSettings(BaseModel):
    """Настройки игры"""

    key = models.CharField(max_length=100, unique=True, verbose_name="Ключ")
    value = models.TextField(verbose_name="Значение")
    value_type = models.CharField(max_length=20, choices=[
        ('string', 'Строка'),
        ('int', 'Целое число'),
        ('float', 'Дробное число'),
        ('bool', 'Логическое'),
        ('json', 'JSON'),
    ], default='string', verbose_name="Тип значения")

    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Настройка игры"
        verbose_name_plural = "Настройки игры"
        ordering = ['key']

    def __str__(self):
        return f"{self.key}: {self.value}"


class GameLog(BaseModel):
    """Логи игровых событий"""

    LOG_TYPES = [
        ('info', 'Информация'),
        ('warning', 'Предупреждение'),
        ('error', 'Ошибка'),
        ('debug', 'Отладка'),
    ]

    level = models.CharField(max_length=20, choices=LOG_TYPES, default='info', verbose_name="Уровень")
    message = models.TextField(verbose_name="Сообщение")
    source = models.CharField(max_length=100, verbose_name="Источник")

    # Связанные объекты (опционально)
    player = models.ForeignKey('accounts.Player', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Игрок")
    character = models.ForeignKey('characters.Character', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Персонаж")

    # Метаданные
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP адрес")
    user_agent = models.TextField(blank=True, verbose_name="User Agent")

    class Meta:
        verbose_name = "Лог игры"
        verbose_name_plural = "Логи игры"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['level', 'created_at']),
            models.Index(fields=['source', 'created_at']),
        ]

    def __str__(self):
        return f"[{self.level.upper()}] {self.source}: {self.message[:50]}"
