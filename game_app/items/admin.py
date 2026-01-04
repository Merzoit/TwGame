from django.contrib import admin
from .models import Item, Inventory


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'rarity', 'item_type', 'equipment_slot', 'value', 'is_equippable', 'is_active']
    list_filter = ['rarity', 'item_type', 'equipment_slot', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']
    ordering = ['name']

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description')
        }),
        ('Свойства предмета', {
            'fields': ('item_type', 'equipment_slot', 'rarity', 'is_active')
        }),
        ('Характеристики', {
            'fields': (
                ('strength_bonus', 'agility_bonus', 'vitality_bonus'),
                ('attack_bonus', 'defense_bonus', 'health_bonus'),
                ('crit_chance_bonus', 'dodge_chance_bonus')
            ),
            'classes': ('collapse',)
        }),
        ('Экономика', {
            'fields': ('value', 'stackable', 'max_stack'),
            'classes': ('collapse',)
        }),
        ('Системная информация', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['player', 'item', 'quantity', 'total_value', 'obtained_at']
    list_filter = ['obtained_at', 'item__rarity', 'item__item_type']
    search_fields = ['player__username', 'player__first_name', 'item__name']
    readonly_fields = ['obtained_at', 'total_value']
    ordering = ['-obtained_at']
