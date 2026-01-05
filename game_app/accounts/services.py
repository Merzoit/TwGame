from .models import Player, PlayerStats
from characters.models import Character, CharacterStats
from items.models import Inventory, PlayerEquipment
from django.utils import timezone


class PlayerService:
    """Сервис для работы с игроками"""

    @staticmethod
    def get_or_create_player(telegram_id, telegram_username=None, twitch_username=None, twitch_id=None):
        """Получить или создать игрока"""
        player, created = Player.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                'telegram_username': telegram_username,
                'twitch_username': twitch_username,
                'twitch_id': twitch_id,
            }
        )

        # Если игрок создан, создаем статистику
        if created:
            PlayerStats.objects.create(player=player)

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
        player = Player.objects.get(telegram_id=telegram_id)

        # Проверяем, нет ли уже персонажа
        if hasattr(player, 'character'):
            raise ValueError("У игрока уже есть персонаж")

        # Создаем персонажа
        character = Character.objects.create(
            player=player,
            name=name
        )

        # Создаем статистику персонажа
        CharacterStats.objects.create(
            character=character,
            strength=strength,
            agility=agility,
            vitality=vitality
        )

        # Создаем экипировку игрока
        PlayerEquipment.objects.create(player=player)

        return character

    @staticmethod
    def get_player_stats(telegram_id):
        """Получить статистику игрока"""
        try:
            player = Player.objects.get(telegram_id=telegram_id)
            return player.stats
        except (Player.DoesNotExist, PlayerStats.DoesNotExist):
            return None

    @staticmethod
    def get_player_inventory(player):
        """Получить инвентарь игрока"""
        return Inventory.objects.filter(player=player).select_related('item')

    @staticmethod
    def get_player_equipment(player):
        """Получить экипировку игрока"""
        try:
            return PlayerEquipment.objects.get(player=player)
        except PlayerEquipment.DoesNotExist:
            # Создаем экипировку, если ее нет
            return PlayerEquipment.objects.create(player=player)

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


