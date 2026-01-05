#!/usr/bin/env python
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'game_app.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'game_app'))
django.setup()

from game.models import Item

# Создаем базовые предметы
items_data = [
    {
        'name': 'Деревянный меч',
        'description': 'Простой деревянный меч для начинающих',
        'item_type': 'weapon',
        'equipment_slot': 'weapon',
        'rarity': 'common',
        'attack_bonus': 5,
        'value': 10,
    },
    {
        'name': 'Железный меч',
        'description': 'Надежный железный меч',
        'item_type': 'weapon',
        'equipment_slot': 'weapon',
        'rarity': 'uncommon',
        'attack_bonus': 12,
        'value': 50,
    },
    {
        'name': 'Кожаная куртка',
        'description': 'Простая кожаная защита',
        'item_type': 'armor',
        'equipment_slot': 'torso',
        'rarity': 'common',
        'defense_bonus': 3,
        'value': 15,
    },
    {
        'name': 'Железная кираса',
        'description': 'Надежная железная броня',
        'item_type': 'armor',
        'equipment_slot': 'torso',
        'rarity': 'uncommon',
        'defense_bonus': 8,
        'health_bonus': 20,
        'value': 80,
    },
    {
        'name': 'Золотая монета',
        'description': 'Ценная золотая монета',
        'item_type': 'resource',
        'equipment_slot': 'none',
        'rarity': 'common',
        'value': 1,
        'stackable': True,
        'max_stack': 999,
    },
]

created_count = 0
for item_data in items_data:
    item, created = Item.objects.get_or_create(
        name=item_data['name'],
        defaults=item_data
    )
    if created:
        created_count += 1
        print(f"Создан предмет: {item.name}")

print(f"Всего создано предметов: {created_count}")
print("Базовые предметы созданы!")



