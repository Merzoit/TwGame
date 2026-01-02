import logging
from .models import Player, PlayerProfile, Character
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
    def create_character(telegram_id, name, class_type):
        """Создает персонажа для игрока"""
        try:
            player = PlayerService.get_player_by_telegram_id(telegram_id)
            if not player:
                logger.error(f"Player {telegram_id} not found")
                return None

            if hasattr(player, 'character') and player.character is not None:
                logger.warning(f"Player {telegram_id} already has character")
                return player.character

            # Проверяем допустимые классы
            valid_classes = ['warrior', 'mage', 'assassin']
            if class_type not in valid_classes:
                logger.error(f"Invalid class type: {class_type}")
                return None

            # Создаем персонажа
            character = Character.objects.create(
                player=player,
                name=name.strip(),
                class_type=class_type
            )

            logger.info(f"Character {character} created for player {telegram_id}")
            return character

        except Exception as e:
            logger.error(f"Error creating character for player {telegram_id}: {e}")
            return None

    @staticmethod
    def get_character_classes():
        """Возвращает доступные классы персонажей"""
        return [
            {
                'type': 'warrior',
                'name': 'Воин',
                'emoji': '⚔️',
                'description': 'Сильный и выносливый боец ближнего боя',
                'image': 'warrior.jpg'
            },
            {
                'type': 'mage',
                'name': 'Маг',
                'emoji': '🔮',
                'description': 'Могучий волшебник с мощными заклинаниями',
                'image': 'mage.jpg'
            },
            {
                'type': 'assassin',
                'name': 'Ассасин',
                'emoji': '🗡️',
                'description': 'Быстрый и скрытный убийца',
                'image': 'assassin.jpg'
            }
        ]
