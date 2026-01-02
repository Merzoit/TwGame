from .models import Player, PlayerProfile
from django.utils import timezone

class PlayerService:
    """Сервис для работы с игроками"""

    @staticmethod
    def get_or_create_player(telegram_id, username=None, first_name=None, last_name=None):
        """
        Получить или создать игрока по Telegram ID
        Возвращает кортеж (player, created)
        """
        player, created = Player.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
            }
        )

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

        # Создаем профиль, если его нет
        if created:
            PlayerProfile.objects.create(player=player)

        # Обновляем время последнего входа
        profile = player.profile
        profile.last_login = timezone.now()
        profile.save()

        return player, created

    @staticmethod
    def get_player_by_telegram_id(telegram_id):
        """Получить игрока по Telegram ID"""
        try:
            return Player.objects.get(telegram_id=telegram_id)
        except Player.DoesNotExist:
            return None

    @staticmethod
    def get_player_profile(telegram_id):
        """Получить профиль игрока по Telegram ID"""
        player = PlayerService.get_player_by_telegram_id(telegram_id)
        if player:
            return player.profile
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
