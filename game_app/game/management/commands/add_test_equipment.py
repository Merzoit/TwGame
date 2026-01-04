from django.core.management.base import BaseCommand
from game.models import Player, Item, Inventory


class Command(BaseCommand):
    help = 'Добавляет тестовые предметы экипировки игроку'

    def add_arguments(self, parser):
        parser.add_argument('--telegram_id', type=str, help='Telegram ID игрока')

    def handle(self, *args, **options):
        telegram_id = options.get('telegram_id')
        if not telegram_id:
            self.stdout.write(self.style.ERROR('Укажите --telegram_id'))
            return

        try:
            player = Player.objects.get(telegram_id=telegram_id)
        except Player.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Игрок с telegram_id {telegram_id} не найден'))
            return

        # Получаем случайные предметы разных редкостей
        test_items = []

        # Серый меч
        gray_weapon = Item.objects.filter(item_type='weapon', rarity='gray').first()
        if gray_weapon:
            test_items.append(gray_weapon)

        # Зеленая броня
        green_armor = Item.objects.filter(item_type='armor', rarity='green').first()
        if green_armor:
            test_items.append(green_armor)

        # Синий предмет
        blue_item = Item.objects.filter(rarity='blue').first()
        if blue_item:
            test_items.append(blue_item)

        # Эпический предмет
        epic_item = Item.objects.filter(rarity='epic').first()
        if epic_item:
            test_items.append(epic_item)

        # Легендарный предмет
        legendary_item = Item.objects.filter(rarity='legendary').first()
        if legendary_item:
            test_items.append(legendary_item)

        added_count = 0
        for item in test_items:
            inventory_item, created = Inventory.objects.get_or_create(
                player=player,
                item=item,
                defaults={'quantity': 1}
            )
            if created:
                added_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Добавлен предмет: {item.name} ({item.get_rarity_display})')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Добавлено предметов: {added_count}')
        )
