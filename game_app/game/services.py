import logging
from .models import Player, PlayerProfile
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
