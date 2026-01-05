from django.contrib import admin
from .models import Character, CharacterStats


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ['name', 'player', 'level', 'experience', 'created_at']
    list_filter = ['level', 'created_at']
    search_fields = ['name', 'player__telegram_username', 'player__telegram_id']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-level', '-experience']

    fieldsets = (
        ('Основная информация', {
            'fields': ('player', 'name', 'level', 'experience')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CharacterStats)
class CharacterStatsAdmin(admin.ModelAdmin):
    list_display = ['character', 'health', 'max_health', 'strength', 'agility', 'vitality', 'min_attack', 'max_attack', 'defense', 'critical_chance', 'dodge_chance']
    list_filter = ['strength', 'agility', 'vitality']
    search_fields = ['character__name', 'character__player__telegram_username']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-character__level']

    fieldsets = (
        ('Персонаж', {
            'fields': ('character',)
        }),
        ('Здоровье', {
            'fields': ('health', 'max_health')
        }),
        ('Основные характеристики', {
            'fields': ('strength', 'agility', 'vitality')
        }),
        ('Бойевые характеристики', {
            'fields': ('min_attack', 'max_attack', 'defense', 'critical_chance', 'dodge_chance')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
