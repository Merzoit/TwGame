import logging
from accounts.models import Player, PlayerStats
from characters.models import Character, CharacterStats
from items.models import PlayerEquipment
from django.utils import timezone

logger = logging.getLogger(__name__)

class PlayerService:
    """Сервис для работы с игроками"""

    @staticmethod
    def get_or_create_player(telegram_id, username=None, first_name=None, last_name=None):
        """
        Получить или создать игрока по Telegram ID
        Возвращает кортеж (player, created)
        """
        try:
            logger.info(f"Attempting to get/create player with telegram_id: {telegram_id}")

            player, created = Player.objects.get_or_create(
                telegram_id=telegram_id,
                defaults={
                    'username': username,
                    'first_name': first_name,
                    'last_name': last_name,
                }
            )

            logger.info(f"Player {'created' if created else 'retrieved'}: {player}")

            # Если игрок уже существует, обновляем его данные
            if not created:
                updated = False
                if username and player.username != username:
                    player.username = username
                    updated = True
                if first_name and player.first_name != first_name:
                    player.first_name = first_name
                    updated = True
                if last_name and player.last_name != last_name:
                    player.last_name = last_name
                    updated = True

                if updated:
                    player.save()
                    logger.info(f"Player {telegram_id} data updated")

            # Создаем профиль, если его нет
            if created:
                profile = PlayerProfile.objects.create(player=player)
                logger.info(f"Profile created for player {telegram_id}: {profile}")

            # Обновляем время последнего входа
            profile = player.profile
            profile.last_login = timezone.now()
            profile.save()
            logger.info(f"Last login updated for player {telegram_id}")

            return player, created

        except Exception as e:
            logger.error(f"Error in get_or_create_player for telegram_id {telegram_id}: {e}")
            raise

    @staticmethod
    def get_player_by_telegram_id(telegram_id):
        """Получить игрока по Telegram ID"""
        try:
            player = Player.objects.get(telegram_id=telegram_id)
            logger.info(f"Found player {telegram_id}: {player}")
            return player
        except Player.DoesNotExist:
            logger.info(f"Player {telegram_id} not found")
            return None
        except Exception as e:
            logger.error(f"Error getting player {telegram_id}: {e}")
            return None

    @staticmethod
    def get_player_profile(telegram_id):
        """Получить профиль игрока по Telegram ID"""
        try:
            player = PlayerService.get_player_by_telegram_id(telegram_id)
            if player:
                profile = player.profile
                logger.info(f"Found profile for player {telegram_id}: {profile}")
                return profile
            logger.info(f"No profile found for player {telegram_id}")
            return None
        except Exception as e:
            logger.error(f"Error getting profile for player {telegram_id}: {e}")
            return None

    @staticmethod
    def update_player_stats(telegram_id, game_result=None, experience_gained=0):
        """
        Обновить статистику игрока
        game_result: 'win', 'loss' или None
        """
        profile = PlayerService.get_player_profile(telegram_id)
        if not profile:
            return False

        # Обновляем опыт
        if experience_gained > 0:
            profile.add_experience(experience_gained)

        # Обновляем статистику игр
        if game_result:
            profile.total_games += 1
            if game_result == 'win':
                profile.wins += 1
            elif game_result == 'loss':
                profile.losses += 1

        profile.save()
        return True

    @staticmethod
    def has_character(telegram_id):
        """Проверяет, есть ли у игрока персонаж"""
        try:
            player = PlayerService.get_player_by_telegram_id(telegram_id)
            if player:
                return hasattr(player, 'character') and player.character is not None
            return False
        except Exception as e:
            logger.error(f"Error checking character for player {telegram_id}: {e}")
            return False

    @staticmethod
    def get_character(telegram_id):
        """Получает персонажа игрока по Telegram ID"""
        try:
            player = PlayerService.get_player_by_telegram_id(telegram_id)
            if player and hasattr(player, 'character'):
                character = player.character
                logger.info(f"Found character {character} for player {telegram_id}")
                return character
            logger.info(f"No character found for player {telegram_id}")
            return None
        except Exception as e:
            logger.error(f"Error getting character for player {telegram_id}: {e}")
            return None

    @staticmethod
    def create_character(telegram_id, name, strength=5, agility=5, vitality=5):
        """Создает персонажа для игрока с заданными навыками"""
        try:
            player = PlayerService.get_player_by_telegram_id(telegram_id)
            if not player:
                logger.error(f"Player {telegram_id} not found")
                return None

            if hasattr(player, 'character') and player.character is not None:
                logger.warning(f"Player {telegram_id} already has character")
                return player.character

            # Проверяем, что сумма навыков равна 20 (15 базовых + 5 свободных)
            total_skill_points = strength + agility + vitality
            if total_skill_points != 20:  # 15 базовых + 5 свободных очков
                logger.error(f"Invalid skill points total: {total_skill_points}")
                return None

            # Проверяем, что каждый навык >= 5
            if strength < 5 or agility < 5 or vitality < 5:
                logger.error(f"Skill points too low: strength={strength}, agility={agility}, vitality={vitality}")
                return None

            # Создаем персонажа
            character = Character.objects.create(
                player=player,
                name=name.strip(),
                strength=strength,
                agility=agility,
                vitality=vitality,
                free_skill_points=0  # Все очки распределены при создании
            )

            logger.info(f"Character {character} created for player {telegram_id}")
            return character

        except Exception as e:
            logger.error(f"Error creating character for player {telegram_id}: {e}")
            return None

    @staticmethod
    def get_skill_info():
        """Возвращает информацию о навыках персонажа"""
        return {
            'strength': {
                'name': 'Сила',
                'emoji': '💪',
                'description': 'Увеличивает максимальную атаку и шанс критического удара',
                'effects': [
                    'Максимальная атака: +3 за уровень',
                    'Шанс крита: +1.5% за уровень'
                ]
            },
            'agility': {
                'name': 'Ловкость',
                'emoji': '🏃',
                'description': 'Увеличивает минимальную атаку и шанс уворота',
                'effects': [
                    'Минимальная атака: +2 за уровень',
                    'Шанс уворота: +1% за уровень'
                ]
            },
            'vitality': {
                'name': 'Живучесть',
                'emoji': '❤️',
                'description': 'Увеличивает здоровье и защиту',
                'effects': [
                    'Здоровье: +15 за уровень',
                    'Защита: +2 за уровень'
                ]
            }
        }

    @staticmethod
    def get_character_equipment(character):
        """Получает экипировку персонажа"""
        equipment_queryset = Equipment.objects.filter(character=character)

        if not equipment_queryset.exists():
            # Создаем пустую экипировку, если ее нет
            return Equipment.objects.create(character=character)

        # Если есть несколько записей, оставляем только первую и удаляем остальные
        equipment = equipment_queryset.first()

        if equipment_queryset.count() > 1:
            logger.warning(f"Found {equipment_queryset.count()} equipment records for character {character}. Keeping first, deleting others.")
            # Удаляем дубликаты, оставляя только первый
            equipment_queryset.exclude(pk=equipment.pk).delete()

        return equipment

    @staticmethod
    def get_player_inventory(player):
        """Получает инвентарь игрока"""
        from .models import Inventory
        return Inventory.objects.filter(player=player).select_related('item')
