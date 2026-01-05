from .models import Player, PlayerProfile
from characters.models import Character, Equipment
from items.models import Inventory
from django.utils import timezone


class PlayerService:
    """Сервис для работы с игроками"""

    @staticmethod
    def get_or_create_player(telegram_id, username=None, first_name=None, last_name=None):
        """Получить или создать игрока"""
        player, created = Player.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
            }
        )

        # Если игрок создан, создаем профиль
        if created:
            PlayerProfile.objects.create(player=player)

        return player, created

    @staticmethod
    def get_character(telegram_id):
        """Получить персонажа игрока по telegram_id"""
        try:
            return Character.objects.select_related('player').get(player__telegram_id=telegram_id)
        except Character.DoesNotExist:
            return None

    @staticmethod
    def has_character(telegram_id):
        """Проверить, есть ли у игрока персонаж"""
        return Character.objects.filter(player__telegram_id=telegram_id).exists()

    @staticmethod
    def create_character(telegram_id, name, strength=5, agility=5, vitality=5):
        """Создать персонажа для игрока"""
        from django.apps import apps
        Character = apps.get_model('characters', 'Character')

        player = Player.objects.get(telegram_id=telegram_id)

        # Проверяем, нет ли уже персонажа
        if hasattr(player, 'character'):
            raise ValueError("У игрока уже есть персонаж")

        character = Character.objects.create(
            player=player,
            name=name,
            strength=strength,
            agility=agility,
            vitality=vitality
        )

        return character

    @staticmethod
    def get_player_profile(telegram_id):
        """Получить профиль игрока"""
        try:
            player = Player.objects.get(telegram_id=telegram_id)
            return player.profile
        except (Player.DoesNotExist, PlayerProfile.DoesNotExist):
            return None

    @staticmethod
    def get_player_inventory(player):
        """Получить инвентарь игрока"""
        return Inventory.objects.filter(player=player).select_related('item')

    @staticmethod
    def get_character_equipment(character):
        """Получить экипировку персонажа"""
        from django.apps import apps
        Equipment = apps.get_model('characters', 'Equipment')

        equipment_queryset = Equipment.objects.filter(character=character)

        if not equipment_queryset.exists():
            # Создаем пустую экипировку, если ее нет
            return Equipment.objects.create(character=character)

        # Если есть несколько записей, оставляем только первую и удаляем остальные
        equipment = equipment_queryset.first()

        if equipment_queryset.count() > 1:
            from core.models import GameLog
            GameLog.objects.create(
                level='warning',
                message=f'Found {equipment_queryset.count()} equipment records for character {character}',
                source='PlayerService.get_character_equipment'
            )
            # Удаляем дубликаты, оставляя только первый
            equipment_queryset.exclude(pk=equipment.pk).delete()

        return equipment

    @staticmethod
    def get_skill_info():
        """Получить информацию о навыках для создания персонажа"""
        return {
            'strength': {
                'name': 'Сила',
                'description': 'Увеличивает урон от оружия и шанс критического удара',
                'icon': '💪'
            },
            'agility': {
                'name': 'Ловкость',
                'description': 'Увеличивает минимальный урон и шанс уклонения',
                'icon': '🏃'
            },
            'vitality': {
                'name': 'Живучесть',
                'description': 'Увеличивает здоровье и защиту',
                'icon': '❤️'
            }
        }

