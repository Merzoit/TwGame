from django.core.management.base import BaseCommand
from game.models import Item
import random


class Command(BaseCommand):
    help = 'Создает предметы экипировки для игры'

    def handle(self, *args, **options):
        # Словарь для описания бонусов по редкости
        rarity_stats = {
            'gray': {'secondary': 1},  # 1 вторичный стат
            'green': {'primary': 1, 'secondary': 1},  # 1 первичный + 1 вторичный
            'blue': {'primary': 1, 'secondary': 2},  # 1 первичный + 2 вторичных
            'epic': {'primary': 2, 'secondary': 2},  # 2 первичных + 2 вторичных
            'legendary': {'primary': 3, 'secondary': 2},  # 3 первичных + 2 вторичных
        }

        # Первичные характеристики
        primary_stats = ['strength', 'agility', 'vitality']

        # Вторичные характеристики
        secondary_stats = ['crit_chance', 'dodge_chance']

        # Базовые предметы для генерации
        weapons = [
            {'base_name': 'Меч', 'attack_base': 5, 'value_base': 10},
            {'base_name': 'Топор', 'attack_base': 8, 'value_base': 15},
            {'base_name': 'Молот', 'attack_base': 6, 'value_base': 12},
            {'base_name': 'Кинжал', 'attack_base': 4, 'value_base': 8},
            {'base_name': 'Посох', 'attack_base': 3, 'value_base': 20},
        ]

        armors = [
            {'base_name': 'Куртка', 'defense_base': 2, 'health_base': 10, 'value_base': 15},
            {'base_name': 'Нагрудник', 'defense_base': 4, 'health_base': 20, 'value_base': 25},
            {'base_name': 'Латы', 'defense_base': 6, 'health_base': 30, 'value_base': 40},
            {'base_name': 'Роба', 'defense_base': 1, 'health_base': 5, 'value_base': 12},
        ]

        # Модификаторы редкости
        rarity_modifiers = {
            'gray': {'stat_mult': 0.5, 'value_mult': 1},
            'green': {'stat_mult': 1, 'value_mult': 2},
            'blue': {'stat_mult': 1.5, 'value_mult': 5},
            'epic': {'stat_mult': 2, 'value_mult': 15},
            'legendary': {'stat_mult': 3, 'value_mult': 50},
        }

        created_count = 0

        # Генерируем оружие
        for weapon in weapons:
            for rarity in ['gray', 'green', 'blue', 'epic', 'legendary']:
                modifier = rarity_modifiers[rarity]
                stats = rarity_stats[rarity]

                item_data = {
                    'name': f'{rarity.title()} {weapon["base_name"]}',
                    'description': f'Предмет редкости {rarity}',
                    'item_type': 'weapon',
                    'equipment_slot': 'weapon',
                    'rarity': rarity,
                    'attack_bonus': int(weapon['attack_base'] * modifier['stat_mult']),
                    'value': int(weapon['value_base'] * modifier['value_mult']),
                    'stackable': False,
                }

                # Добавляем бонусы характеристик
                self.add_stat_bonuses(item_data, stats, primary_stats, secondary_stats, modifier['stat_mult'])

                item, created = Item.objects.get_or_create(
                    name=item_data['name'],
                    defaults=item_data
                )
                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Создано оружие: {item.name}')
                    )

        # Генерируем броню
        for armor in armors:
            for rarity in ['gray', 'green', 'blue', 'epic', 'legendary']:
                modifier = rarity_modifiers[rarity]
                stats = rarity_stats[rarity]

                item_data = {
                    'name': f'{rarity.title()} {armor["base_name"]}',
                    'description': f'Предмет редкости {rarity}',
                    'item_type': 'armor',
                    'equipment_slot': 'torso',
                    'rarity': rarity,
                    'defense_bonus': int(armor['defense_base'] * modifier['stat_mult']),
                    'health_bonus': int(armor['health_base'] * modifier['stat_mult']),
                    'value': int(armor['value_base'] * modifier['value_mult']),
                    'stackable': False,
                }

                # Добавляем бонусы характеристик
                self.add_stat_bonuses(item_data, stats, primary_stats, secondary_stats, modifier['stat_mult'])

                item, created = Item.objects.get_or_create(
                    name=item_data['name'],
                    defaults=item_data
                )
                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Создана броня: {item.name}')
                    )

        # Создаем золотую монету
        Item.objects.get_or_create(
            name='Золотая монета',
            defaults={
                'description': 'Ценная золотая монета',
                'item_type': 'resource',
                'equipment_slot': 'none',
                'rarity': 'gray',
                'value': 1,
                'stackable': True,
                'max_stack': 999,
            }
        )

        self.stdout.write(
            self.style.SUCCESS(f'Всего создано предметов: {created_count}')
        )

    def add_stat_bonuses(self, item_data, stats, primary_stats, secondary_stats, multiplier):
        """Добавляет бонусы характеристик к предмету"""
        # Выбираем случайные первичные характеристики
        if 'primary' in stats:
            primary_count = stats['primary']
            selected_primary = random.sample(primary_stats, primary_count)
            for stat in selected_primary:
                bonus_name = f'{stat}_bonus'
                # Случайный бонус от 1 до 3, умноженный на модификатор редкости
                bonus_value = random.randint(1, 3) * multiplier
                item_data[bonus_name] = int(bonus_value)

        # Выбираем случайные вторичные характеристики
        if 'secondary' in stats:
            secondary_count = stats['secondary']
            selected_secondary = random.sample(secondary_stats, secondary_count)
            for stat in selected_secondary:
                bonus_name = f'{stat}_bonus'
                # Случайный бонус от 0.5% до 2%, умноженный на модификатор редкости
                bonus_value = random.uniform(0.5, 2.0) * multiplier
                item_data[bonus_name] = round(bonus_value, 1)

