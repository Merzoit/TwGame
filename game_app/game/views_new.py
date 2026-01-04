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

                # Автоматически создаем слоты экипировки для персонажа, если их нет
                from game.models import Equipment
                if not character.equipment.exists():
                    Equipment.objects.create(character=character, slot='weapon')
                    Equipment.objects.create(character=character, slot='torso')

                # Получаем инвентарь игрока
                inventory = player.inventory.all().select_related('item') if hasattr(player, 'inventory') else []
                equipment = PlayerService.get_character_equipment(character)

                # Получаем экипировку персонажа
                equipment = character.equipment.all().select_related('item') if hasattr(character, 'equipment') else []

                return render(request, 'game/game.html', {
                    'game_name': 'TwGame',
                    'version': '0.1.0',
                    'character': character,
                    'profile': profile,
                    'player': player,
                    'next_level_exp': next_level_exp,
                    'progress_percentage': progress_percentage,
                    'inventory': inventory,
                    'equipment': equipment,
                })
            else:
                # Персонажа нет - показываем страницу создания персонажа
                skill_info = PlayerService.get_skill_info()

                # Конвертируем user_data в JSON для безопасной передачи в JavaScript
                telegram_user_json = json.dumps(user_data, ensure_ascii=False)

                return render(request, 'game/create_character.html', {
                    'game_name': 'TwGame',
                    'version': '0.1.0',
                    'skill_info': skill_info,
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
        strength = int(data.get('strength', 5))
        agility = int(data.get('agility', 5))
        vitality = int(data.get('vitality', 5))

        if not all([telegram_id, character_name]):
            return JsonResponse({'success': False, 'error': 'Недостаточно данных'})

        # Проверяем, существует ли уже персонаж с таким именем
        from .models import Character
        if Character.objects.filter(name__iexact=character_name).exists():
            return JsonResponse({'success': False, 'error': f'Персонаж с именем "{character_name}" уже существует. Выберите другое имя.'})

        # Проверяем валидность навыков
        if strength < 5 or agility < 5 or vitality < 5:
            return JsonResponse({'success': False, 'error': 'Каждый навык должен быть не меньше 5'})

        total_points = strength + agility + vitality
        if total_points != 20:  # 15 базовых + 5 свободных очков
            return JsonResponse({'success': False, 'error': f'Общее количество очков навыков должно быть 20 (текущее: {total_points})'})

        # Создаем персонажа
        character = PlayerService.create_character(
            telegram_id=telegram_id,
            name=character_name,
            strength=strength,
            agility=agility,
            vitality=vitality
        )

        if character:
            return JsonResponse({
                'success': True,
                'character': {
                    'id': character.id,
                    'name': character.name,
                    'level': character.level,
                    'max_health': character.max_health,
                    'min_attack': character.min_attack,
                    'max_attack': character.max_attack,
                    'defense': character.defense,
                    'strength': character.strength,
                    'agility': character.agility,
                    'vitality': character.vitality,
                }
            })
        else:
            return JsonResponse({'success': False, 'error': 'Не удалось создать персонажа'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@require_GET
def api_status(request):
    """API статус"""
    return JsonResponse({'status': 'ok'})


@csrf_exempt
@require_POST
def telegram_webhook(request):
    """Обработка вебхуков от Telegram"""
    try:
        import json
        data = json.loads(request.body)
        # Обработка данных от Telegram
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'error': str(e)})


# Admin Panel Views
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Player, Character, Item, Inventory, Equipment
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def admin_dashboard(request):
    """Главная страница админ панели"""
    stats = {
        'players_count': Player.objects.count(),
        'characters_count': Character.objects.count(),
        'items_count': Item.objects.count(),
        'inventory_count': Inventory.objects.count(),
    }

    return render(request, 'game/admin/dashboard.html', {
        'stats': stats,
        'active_tab': 'dashboard'
    })

def admin_players(request):
    """Управление игроками"""
    search_query = request.GET.get('search', '')
    page = request.GET.get('page', 1)

    players = Player.objects.all()

    if search_query:
        players = players.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(username__icontains=search_query) |
            Q(telegram_id__icontains=search_query)
        )

    paginator = Paginator(players.order_by('-id'), 20)
    players_page = paginator.get_page(page)

    return render(request, 'game/admin/players.html', {
        'players': players_page,
        'search_query': search_query,
        'active_tab': 'players'
    })

def admin_player_detail(request, player_id):
    """Детальная информация об игроке"""
    player = get_object_or_404(Player, id=player_id)
    character = PlayerService.get_character(player.telegram_id)
    inventory = PlayerService.get_player_inventory(player)
    equipment = PlayerService.get_character_equipment(character) if character else None

    return render(request, 'game/admin/player_detail.html', {
        'player': player,
        'character': character,
        'inventory': inventory,
        'equipment': equipment,
        'active_tab': 'players'
    })

def admin_characters(request):
    """Управление персонажами"""
    search_query = request.GET.get('search', '')
    page = request.GET.get('page', 1)

    characters = Character.objects.select_related('player').all()

    if search_query:
        characters = characters.filter(
            Q(name__icontains=search_query) |
            Q(player__first_name__icontains=search_query) |
            Q(player__username__icontains=search_query)
        )

    paginator = Paginator(characters.order_by('-id'), 20)
    characters_page = paginator.get_page(page)

    return render(request, 'game/admin/characters.html', {
        'characters': characters_page,
        'search_query': search_query,
        'active_tab': 'characters'
    })

def admin_character_detail(request, character_id):
    """Детальная информация о персонаже"""
    character = get_object_or_404(Character, id=character_id)
    equipment = PlayerService.get_character_equipment(character)

    return render(request, 'game/admin/character_detail.html', {
        'character': character,
        'equipment': equipment,
        'active_tab': 'characters'
    })

def admin_items(request):
    """Управление предметами"""
    search_query = request.GET.get('search', '')
    rarity_filter = request.GET.get('rarity', '')
    type_filter = request.GET.get('type', '')
    page = request.GET.get('page', 1)

    items = Item.objects.all()

    if search_query:
        items = items.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if rarity_filter:
        items = items.filter(rarity=rarity_filter)

    if type_filter:
        items = items.filter(item_type=type_filter)

    paginator = Paginator(items.order_by('-id'), 20)
    items_page = paginator.get_page(page)

    rarities = Item.RARITIES
    types = Item.TYPES

    return render(request, 'game/admin/items.html', {
        'items': items_page,
        'search_query': search_query,
        'rarity_filter': rarity_filter,
        'type_filter': type_filter,
        'rarities': rarities,
        'types': types,
        'active_tab': 'items'
    })

def admin_item_detail(request, item_id):
    """Детальная информация о предмете"""
    item = get_object_or_404(Item, id=item_id)

    return render(request, 'game/admin/item_detail.html', {
        'item': item,
        'active_tab': 'items'
    })

def admin_item_create(request):
    """Создание нового предмета"""
    if request.method == 'POST':
        try:
            # Получаем данные из формы
            name = request.POST.get('name', '').strip()
            description = request.POST.get('description', '').strip()
            rarity = request.POST.get('rarity', '')
            item_type = request.POST.get('item_type', '')
            equipment_slot = request.POST.get('equipment_slot', '')
            value = int(request.POST.get('value', 0))

            # Бонусы характеристик
            attack_bonus = int(request.POST.get('attack_bonus', 0))
            defense_bonus = int(request.POST.get('defense_bonus', 0))
            health_bonus = int(request.POST.get('health_bonus', 0))
            crit_chance_bonus = float(request.POST.get('crit_chance_bonus', 0))
            dodge_chance_bonus = float(request.POST.get('dodge_chance_bonus', 0))

            # Основные характеристики
            strength_bonus = int(request.POST.get('strength_bonus', 0))
            agility_bonus = int(request.POST.get('agility_bonus', 0))
            vitality_bonus = int(request.POST.get('vitality_bonus', 0))

            is_equippable = request.POST.get('is_equippable') == 'on'

            # Валидация обязательных полей
            if not all([name, description, rarity, item_type]):
                messages.error(request, 'Пожалуйста, заполните все обязательные поля!')
                return redirect('game:admin_item_create')

            # Создаем предмет
            item = Item.objects.create(
                name=name,
                description=description,
                rarity=rarity,
                item_type=item_type,
                equipment_slot=equipment_slot if equipment_slot else None,
                value=value,
                attack_bonus=attack_bonus,
                defense_bonus=defense_bonus,
                health_bonus=health_bonus,
                crit_chance_bonus=crit_chance_bonus,
                dodge_chance_bonus=dodge_chance_bonus,
                strength_bonus=strength_bonus,
                agility_bonus=agility_bonus,
                vitality_bonus=vitality_bonus,
                is_equippable=is_equippable
            )

            messages.success(request, f'Предмет "{name}" успешно создан!')
            return redirect('game:admin_item_detail', item_id=item.id)

        except Exception as e:
            messages.error(request, f'Ошибка при создании предмета: {str(e)}')
            return redirect('game:admin_item_create')

    rarities = Item.RARITIES
    types = Item.TYPES

    return render(request, 'game/admin/item_create.html', {
        'rarities': rarities,
        'types': types,
        'active_tab': 'items'
    })

def admin_inventory(request):
    """Управление инвентарем"""
    search_query = request.GET.get('search', '')
    page = request.GET.get('page', 1)

    inventory = Inventory.objects.select_related('player', 'item').all()

    if search_query:
        inventory = inventory.filter(
            Q(player__first_name__icontains=search_query) |
            Q(player__username__icontains=search_query) |
            Q(item__name__icontains=search_query)
        )

    paginator = Paginator(inventory.order_by('-id'), 20)
    inventory_page = paginator.get_page(page)

    return render(request, 'game/admin/inventory.html', {
        'inventory': inventory_page,
        'search_query': search_query,
        'active_tab': 'inventory'
    })

def admin_equipment(request):
    """Управление экипировкой"""
    search_query = request.GET.get('search', '')
    page = request.GET.get('page', 1)

    equipment = Equipment.objects.select_related('character', 'character__player', 'weapon', 'torso').all()

    if search_query:
        equipment = equipment.filter(
            Q(character__name__icontains=search_query) |
            Q(character__player__first_name__icontains=search_query) |
            Q(character__player__username__icontains=search_query)
        )

    paginator = Paginator(equipment.order_by('-id'), 20)
    equipment_page = paginator.get_page(page)

    return render(request, 'game/admin/equipment.html', {
        'equipment': equipment_page,
        'search_query': search_query,
        'active_tab': 'equipment'
    })


# Twitch OAuth
@require_GET
def twitch_auth(request):
    """Инициирует авторизацию через Twitch"""
    import secrets
    import urllib.parse

    # Генерируем state для защиты от CSRF
    state = secrets.token_urlsafe(32)
    request.session['twitch_oauth_state'] = state

    # Параметры для авторизации
    client_id = 'duwoiegw4pnse0gq7c7oradhwdslah'
    redirect_uri = request.build_absolute_uri('/api/auth/twitch/callback/')
    scope = 'user:read:email'

    auth_url = (
        f'https://id.twitch.tv/oauth2/authorize?'
        f'client_id={client_id}&'
        f'redirect_uri={urllib.parse.quote(redirect_uri)}&'
        f'response_type=code&'
        f'scope={scope}&'
        f'state={state}'
    )

    return redirect(auth_url)


@require_GET
def twitch_callback(request):
    """Обработка callback от Twitch"""
    import requests
    import urllib.parse

    code = request.GET.get('code')
    state = request.GET.get('state')
    error = request.GET.get('error')

    # Проверяем state для защиты от CSRF
    saved_state = request.session.get('twitch_oauth_state')
    if not state or state != saved_state:
        return render(request, 'game/error.html', {
            'error_message': 'Ошибка безопасности: неверный state'
        })

    if error:
        return render(request, 'game/error.html', {
            'error_message': f'Ошибка авторизации Twitch: {error}'
        })

    if not code:
        return render(request, 'game/error.html', {
            'error_message': 'Код авторизации не получен'
        })

    try:
        # Обмениваем код на токен доступа
        client_id = 'duwoiegw4pnse0gq7c7oradhwdslah'
        client_secret = '01us0o6obskm3hh008yyw0y4rkcyzy'
        redirect_uri = request.build_absolute_uri('/api/auth/twitch/callback/')

        token_response = requests.post('https://id.twitch.tv/oauth2/token', data={
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri
        })

        if token_response.status_code != 200:
            return render(request, 'game/error.html', {
                'error_message': 'Не удалось получить токен доступа'
            })

        token_data = token_response.json()
        access_token = token_data.get('access_token')

        # Получаем информацию о пользователе
        user_response = requests.get('https://api.twitch.tv/helix/users', headers={
            'Authorization': f'Bearer {access_token}',
            'Client-Id': client_id
        })

        if user_response.status_code != 200:
            return render(request, 'game/error.html', {
                'error_message': 'Не удалось получить данные пользователя'
            })

        user_data = user_response.json()
        if not user_data.get('data'):
            return render(request, 'game/error.html', {
                'error_message': 'Данные пользователя не найдены'
            })

        twitch_user = user_data['data'][0]
        twitch_username = twitch_user.get('login')
        twitch_id = twitch_user.get('id')

        # Сохраняем данные в сессии для использования в игре
        request.session['twitch_connected'] = True
        request.session['twitch_username'] = twitch_username
        request.session['twitch_id'] = twitch_id

        # Перенаправляем обратно в игру
        return redirect('/')

    except Exception as e:
        return render(request, 'game/error.html', {
            'error_message': f'Ошибка при обработке авторизации: {str(e)}'
        })


@csrf_exempt
@require_POST
def api_status(request):
    """API статус"""
    return JsonResponse({'status': 'ok'})


@csrf_exempt
@require_POST
def telegram_webhook(request):
    """Обработка вебхуков от Telegram"""
    try:
        import json
        data = json.loads(request.body)
        # Обработка данных от Telegram
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'error': str(e)})


@csrf_exempt
@require_POST
def equip_item(request):
    """Экипировка предмета"""
    try:
        import json
        data = json.loads(request.body)

        telegram_id = data.get('telegram_id')
        item_id = data.get('item_id')
        slot = data.get('slot')

        if not all([telegram_id, item_id, slot]):
            return JsonResponse({'success': False, 'error': 'Отсутствуют необходимые данные'})

        # Получаем персонажа
        character = PlayerService.get_character(telegram_id)
        if not character:
            return JsonResponse({'success': False, 'error': 'Персонаж не найден'})

        # Получаем предмет из инвентаря
        inventory_item = Inventory.objects.filter(player__telegram_id=telegram_id, item_id=item_id).first()
        if not inventory_item:
            return JsonResponse({'success': False, 'error': 'Предмет не найден в инвентаре'})

        # Получаем экипировку персонажа
        equipment = PlayerService.get_character_equipment(character)

        # Экипируем предмет
        if slot == 'weapon':
            equipment.weapon = inventory_item.item
        elif slot == 'torso':
            equipment.torso = inventory_item.item
        else:
            return JsonResponse({'success': False, 'error': 'Неверный слот'})

        equipment.save()

        # Уменьшаем количество предметов в инвентаре
        inventory_item.quantity -= 1
        if inventory_item.quantity <= 0:
            inventory_item.delete()
        else:
            inventory_item.save()

        # Пересчитываем характеристики персонажа
        character.save()

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
@require_POST
def unequip_item(request):
    """Снятие предмета с экипировки"""
    try:
        import json
        data = json.loads(request.body)

        telegram_id = data.get('telegram_id')
        slot = data.get('slot')

        if not all([telegram_id, slot]):
            return JsonResponse({'success': False, 'error': 'Отсутствуют необходимые данные'})

        # Получаем персонажа
        character = PlayerService.get_character(telegram_id)
        if not character:
            return JsonResponse({'success': False, 'error': 'Персонаж не найден'})

        # Получаем экипировку персонажа
        equipment = PlayerService.get_character_equipment(character)

        # Снимаем предмет из слота
        if slot == 'weapon':
            equipment.weapon = None
        elif slot == 'torso':
            equipment.torso = None
        else:
            return JsonResponse({'success': False, 'error': 'Неверный слот'})

        equipment.save()

        # Пересчитываем характеристики персонажа
        character.save()

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})