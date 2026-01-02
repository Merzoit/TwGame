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
            # Получаем или создаем игрока
            player, created = PlayerService.get_or_create_player(
                telegram_id=telegram_id,
                username=user_data.get('username'),
                first_name=user_data.get('first_name'),
                last_name=user_data.get('last_name')
            )

            # Проверяем, есть ли у пользователя персонаж
            has_character = PlayerService.has_character(telegram_id)

            if has_character:
                # Персонаж есть - показываем игровое меню
                character = PlayerService.get_character(telegram_id)
                profile = PlayerService.get_player_profile(telegram_id)

                # Вычисляем прогресс до следующего уровня
                next_level_exp = character.level * 100
                progress_percentage = (character.experience / next_level_exp * 100) if next_level_exp > 0 else 0

                return render(request, 'game/game.html', {
                    'game_name': 'TwGame',
                    'version': '0.1.0',
                    'character': character,
                    'profile': profile,
                    'player': player,
                    'next_level_exp': next_level_exp,
                    'progress_percentage': progress_percentage,
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

        # Проверяем, существует ли уже персонаж с таким именем
        from .models import Character
        if Character.objects.filter(name__iexact=character_name).exists():
            return JsonResponse({'success': False, 'error': f'Персонаж с именем "{character_name}" уже существует. Выберите другое имя.'})

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

# Twitch OAuth Views
import os
import secrets
import requests
from urllib.parse import urlencode
from django.shortcuts import redirect
from django.urls import reverse

TWITCH_CLIENT_ID = os.environ.get('TWITCH_CLIENT_ID', '')
TWITCH_CLIENT_SECRET = os.environ.get('TWITCH_CLIENT_SECRET', '')
TWITCH_REDIRECT_URI = os.environ.get('TWITCH_REDIRECT_URI', '')

@require_GET
def twitch_auth(request):
    """Начало авторизации через Twitch"""
    telegram_user = request.GET.get('user')
    if not telegram_user:
        return redirect('/')

    # Генерируем state для защиты от CSRF
    state = secrets.token_urlsafe(32)

    # Сохраняем state в сессии вместе с telegram_user
    request.session['twitch_oauth_state'] = state
    request.session['twitch_telegram_user'] = telegram_user

    # Параметры для Twitch OAuth
    params = {
        'client_id': TWITCH_CLIENT_ID,
        'redirect_uri': TWITCH_REDIRECT_URI,
        'response_type': 'code',
        'scope': 'user:read:email',
        'state': state
    }

    auth_url = f"https://id.twitch.tv/oauth2/authorize?{urlencode(params)}"
    return redirect(auth_url)

@require_GET
def twitch_callback(request):
    """Обработка callback от Twitch"""
    code = request.GET.get('code')
    state = request.GET.get('state')
    error = request.GET.get('error')

    # Проверяем ошибки
    if error:
        return render(request, 'game/error.html', {
            'error_message': f'Ошибка авторизации Twitch: {error}'
        })

    if not code:
        return render(request, 'game/error.html', {
            'error_message': 'Не получен код авторизации от Twitch'
        })

    # Проверяем state для защиты от CSRF
    session_state = request.session.get('twitch_oauth_state')
    telegram_user = request.session.get('twitch_telegram_user')

    if not session_state or not telegram_user or state != session_state:
        return render(request, 'game/error.html', {
            'error_message': 'Неверный state токен. Попробуйте авторизацию заново.'
        })

    try:
        # Обмениваем код на токен доступа
        token_data = {
            'client_id': TWITCH_CLIENT_ID,
            'client_secret': TWITCH_CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': TWITCH_REDIRECT_URI
        }

        token_response = requests.post('https://id.twitch.tv/oauth2/token', data=token_data)
        token_response.raise_for_status()
        token_json = token_response.json()

        access_token = token_json.get('access_token')
        if not access_token:
            return render(request, 'game/error.html', {
                'error_message': 'Не удалось получить токен доступа от Twitch'
            })

        # Получаем информацию о пользователе
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Client-Id': TWITCH_CLIENT_ID
        }

        user_response = requests.get('https://api.twitch.tv/helix/users', headers=headers)
        user_response.raise_for_status()
        user_data = user_response.json()

        if not user_data.get('data'):
            return render(request, 'game/error.html', {
                'error_message': 'Не удалось получить данные пользователя от Twitch'
            })

        twitch_user = user_data['data'][0]
        twitch_username = twitch_user['login']
        twitch_id = twitch_user['id']

        # Сохраняем данные в базу данных
        telegram_data = json.loads(telegram_user)
        telegram_id = telegram_data.get('id')

        if telegram_id:
            player, created = PlayerService.get_or_create_player(
                telegram_id=telegram_id,
                username=telegram_data.get('username'),
                first_name=telegram_data.get('first_name'),
                last_name=telegram_data.get('last_name')
            )

            # Обновляем Twitch данные
            player.twitch_username = twitch_username
            player.twitch_id = twitch_id
            player.twitch_access_token = access_token
            player.twitch_refresh_token = token_json.get('refresh_token')
            player.twitch_connected = True
            player.save()

        # Очищаем сессию
        del request.session['twitch_oauth_state']
        del request.session['twitch_telegram_user']

        # Перенаправляем обратно в игру
        return redirect(f"/?user={telegram_user}")

    except requests.RequestException as e:
        return render(request, 'game/error.html', {
            'error_message': f'Ошибка при подключении к Twitch: {str(e)}'
        })
    except Exception as e:
        return render(request, 'game/error.html', {
            'error_message': f'Неожиданная ошибка: {str(e)}'
        })
