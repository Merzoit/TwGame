from django.contrib import admin
from .models import Character, Equipment


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ['name', 'player', 'level', 'strength', 'agility', 'vitality', 'max_health', 'created_at']
    list_filter = ['level', 'created_at']
    search_fields = ['name', 'player__username', 'player__first_name', 'player__telegram_id']
    readonly_fields = ['created_at', 'updated_at', 'max_health', 'min_attack', 'max_attack', 'defense', 'crit_chance', 'dodge_chance']
    ordering = ['-level', '-created_at']

    fieldsets = (
        ('Основная информация', {
            'fields': ('player', 'name')
        }),
        ('Навыки', {
            'fields': ('strength', 'agility', 'vitality', 'free_skill_points')
        }),
        ('Характеристики', {
            'fields': ('level', 'experience', 'max_health', 'current_health')
        }),
        ('Бойевые параметры', {
            'fields': ('min_attack', 'max_attack', 'defense', 'crit_chance', 'dodge_chance'),
            'classes': ('collapse',)
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['character', 'slot', 'item', 'equipped_at']
    list_filter = ['slot', 'equipped_at']
    search_fields = ['character__name', 'item__name']
    readonly_fields = ['equipped_at']
    ordering = ['-equipped_at']
