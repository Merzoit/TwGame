from django.core.management.base import BaseCommand
from game.models import Item


class Command(BaseCommand):
    help = 'Создает базовые предметы для игры'

    def handle(self, *args, **options):
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
                self.stdout.write(
                    self.style.SUCCESS(f'Создан предмет: {item.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Всего создано предметов: {created_count}')
        )
