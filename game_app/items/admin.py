from django.contrib import admin
from .models import Item, EquipmentItems, CraftItems, Inventory, PlayerEquipment


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'item_type', 'value', 'is_active', 'created_at']
    list_filter = ['item_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']
    ordering = ['name']

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'item_type', 'cost')
        }),
        ('Системная информация', {
            'fields': ('is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(EquipmentItems)
class EquipmentItemsAdmin(admin.ModelAdmin):
    list_display = ['item', 'equipment_slot', 'rarity', 'level_requirement', 'strength_bonus', 'agility_bonus', 'vitality_bonus']
    list_filter = ['equipment_slot', 'rarity', 'level_requirement']
    search_fields = ['item__name', 'item__description']
    ordering = ['item__name']

    fieldsets = (
        ('Предмет', {
            'fields': ('item',)
        }),
        ('Экипировка', {
            'fields': ('equipment_slot', 'rarity', 'level_requirement')
        }),
        ('Бонусы к характеристикам', {
            'fields': (
                ('strength_bonus', 'agility_bonus', 'vitality_bonus'),
                ('attack_bonus', 'defense_bonus', 'health_bonus'),
                ('crit_chance_bonus', 'dodge_chance_bonus')
            )
        }),
    )


@admin.register(CraftItems)
class CraftItemsAdmin(admin.ModelAdmin):
    list_display = ['item', 'stack_size', 'is_craftable']
    list_filter = ['is_craftable', 'stack_size']
    search_fields = ['item__name', 'item__description']
    ordering = ['item__name']

    fieldsets = (
        ('Предмет', {
            'fields': ('item',)
        }),
        ('Свойства крафта', {
            'fields': ('stack_size', 'is_craftable')
        }),
    )


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['player', 'item', 'quantity', 'is_equipped', 'equipped_slot', 'created_at']
    list_filter = ['is_equipped', 'equipped_slot', 'created_at', 'item__item_type']
    search_fields = ['player__telegram_username', 'player__telegram_id', 'item__name']
    readonly_fields = ['created_at']
    ordering = ['-created_at']

    fieldsets = (
        ('Игрок и предмет', {
            'fields': ('player', 'item', 'quantity')
        }),
        ('Экипировка', {
            'fields': ('is_equipped', 'equipped_slot')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PlayerEquipment)
class PlayerEquipmentAdmin(admin.ModelAdmin):
    list_display = ['player', 'weapon_slot', 'head_slot', 'body_slot', 'hands_slot', 'feet_slot', 'created_at']
    search_fields = ['player__telegram_username', 'player__telegram_id']
    readonly_fields = ['created_at']
    ordering = ['-created_at']

    fieldsets = (
        ('Игрок', {
            'fields': ('player',)
        }),
        ('Экипировка', {
            'fields': (
                ('weapon_slot', 'head_slot'),
                ('body_slot', 'legs_slot'),
                ('hands_slot', 'feet_slot'),
                ('amulet_slot', 'ring_slot')
            )
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
