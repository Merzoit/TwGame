#!/usr/bin/env python
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'game_app.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'game_app'))
django.setup()

from game.models import Player, Inventory, Equipment, Item

def add_test_data():
    # Получаем первого игрока
    try:
        player = Player.objects.first()
        if not player:
            print("Игроков не найдено")
            return

        print(f"Добавляем тестовые данные для игрока: {player.username or player.first_name}")

        # Добавляем предметы в инвентарь
        items_to_add = [
            ('Деревянный меч', 1),
            ('Кожаная куртка', 1),
            ('Золотая монета', 50),
        ]

        for item_name, quantity in items_to_add:
            try:
                item = Item.objects.get(name=item_name)
                inventory_item, created = Inventory.objects.get_or_create(
                    player=player,
                    item=item,
                    defaults={'quantity': quantity}
                )
                if created:
                    print(f"Добавлен в инвентарь: {item_name} x{quantity}")
                else:
                    print(f"Уже есть в инвентаре: {item_name}")
            except Item.DoesNotExist:
                print(f"Предмет не найден: {item_name}")

        # Создаем слоты экипировки для персонажа
        if hasattr(player, 'character') and player.character:
            character = player.character
            print(f"Создаем слоты экипировки для персонажа: {character.name}")

            # Создаем слоты
            slots = ['weapon', 'torso']
            for slot in slots:
                equipment, created = Equipment.objects.get_or_create(
                    character=character,
                    slot=slot
                )
                if created:
                    print(f"Создан слот экипировки: {slot}")
                else:
                    print(f"Слот уже существует: {slot}")
        else:
            print("У игрока нет персонажа")

        print("Тестовые данные добавлены!")

    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == '__main__':
    add_test_data()



