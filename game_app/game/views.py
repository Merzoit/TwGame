from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from .services import PlayerService
import json

# Create your views here.

@require_GET
def home(request):
    """Главная страница игры"""
    # Проверяем, авторизован ли пользователь через Telegram
    telegram_user = request.GET.get('user')
    if not telegram_user:
        # Если пользователь не авторизован, показываем стартовую страницу
        return render(request, 'game/welcome.html', {
            'game_name': 'TwGame',
            'version': '0.1.0',
        })

                # Парсим данные пользователя из Telegram (URL-decoded)
    try:
        import json
        import urllib.parse
        decoded_user = urllib.parse.unquote(telegram_user)
        user_data = json.loads(decoded_user)
        telegram_id = user_data.get('id')

        if telegram_id:
            # Проверяем, есть ли у пользователя персонаж
            has_character = PlayerService.has_character(telegram_id)

            if has_character:
                # Персонаж есть - показываем игровое меню
                character = PlayerService.get_character(telegram_id)
                profile = PlayerService.get_player_profile(telegram_id)

                return render(request, 'game/game.html', {
                    'game_name': 'TwGame',
                    'version': '0.1.0',
                    'character': character,
                    'profile': profile,
                })
            else:
                # Персонажа нет - показываем страницу создания персонажа
                character_classes = PlayerService.get_character_classes()

                # Конвертируем user_data в JSON для безопасной передачи в JavaScript
                telegram_user_json = json.dumps(user_data, ensure_ascii=False)

                return render(request, 'game/create_character.html', {
                    'game_name': 'TwGame',
                    'version': '0.1.0',
                    'character_classes': character_classes,
                    'telegram_user_json': telegram_user_json,
                })
        else:
            return render(request, 'game/error.html', {
                'error_message': 'Неверные данные пользователя Telegram'
            })

    except Exception as e:
        return render(request, 'game/error.html', {
            'error_message': f'Ошибка обработки данных: {str(e)}'
        })

@csrf_exempt
@require_POST
def create_character(request):
    """Создание персонажа"""
    try:
        import json
        data = json.loads(request.body)

        telegram_id = data.get('telegram_id')
        character_name = data.get('name')
        class_type = data.get('class_type')

        if not all([telegram_id, character_name, class_type]):
            return JsonResponse({'success': False, 'error': 'Недостаточно данных'})

        # Создаем персонажа
        character = PlayerService.create_character(
            telegram_id=telegram_id,
            name=character_name,
            class_type=class_type
        )

        if character:
            return JsonResponse({
                'success': True,
                'character': {
                    'id': character.id,
                    'name': character.name,
                    'class_display_name': character.class_display_name,
                    'level': character.level,
                    'max_health': character.max_health,
                    'attack_power': character.attack_power,
                    'defense': character.defense,
                }
            })
        else:
            return JsonResponse({'success': False, 'error': 'Не удалось создать персонажа'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@require_GET
def api_status(request):
    """API статус"""
    return JsonResponse({
        'status': 'online',
        'game': 'TwGame',
        'version': '0.1.0',
    })

@csrf_exempt
@require_POST
def telegram_webhook(request):
    """Вебхук для Telegram бота"""
    try:
        data = json.loads(request.body)
        # Здесь будет обработка данных от Telegram
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
