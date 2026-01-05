from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from accounts.models import Player, PlayerStats
from characters.models import Character, CharacterStats
from items.models import Item, Inventory, EquipmentItems, CraftItems, PlayerEquipment

from accounts.services import PlayerService

# Admin Panel Views

@login_required
def admin_dashboard(request):
    """Главная страница админ панели"""
    try:
        stats = {
            'players_count': Player.objects.count(),
            'characters_count': Character.objects.count(),
            'items_count': Item.objects.count(),
            'inventory_count': Inventory.objects.count(),
        }
    except Exception as e:
        # Если есть проблемы с моделями, возвращаем заглушку
        stats = {
            'players_count': 0,
            'characters_count': 0,
            'items_count': 0,
            'inventory_count': 0,
        }

    return render(request, 'admin_panel/dashboard.html', {
        'stats': stats,
        'active_tab': 'dashboard'
    })

@login_required
def admin_players(request):
    """Управление игроками"""
    search_query = request.GET.get('search', '')
    page = request.GET.get('page', 1)

    players = Player.objects.all()

    if search_query:
        players = players.filter(
            Q(telegram_username__icontains=search_query) |
            Q(twitch_username__icontains=search_query) |
            Q(telegram_id__icontains=search_query) |
            Q(twitch_id__icontains=search_query)
        )

    paginator = Paginator(players.order_by('-id'), 20)
    players_page = paginator.get_page(page)

    return render(request, 'admin_panel/players.html', {
        'players': players_page,
        'search_query': search_query,
        'active_tab': 'players'
    })

@login_required
def admin_player_detail(request, player_id):
    """Детальная информация об игроке"""
    player = get_object_or_404(Player, id=player_id)
    stats = player.stats if hasattr(player, 'stats') else None
    character = player.character if hasattr(player, 'character') else None
    inventory = player.inventory.all() if hasattr(player, 'inventory') else []
    equipment = player.equipment if hasattr(player, 'equipment') else None

    return render(request, 'admin_panel/player_detail.html', {
        'player': player,
        'stats': stats,
        'character': character,
        'inventory': inventory,
        'equipment': equipment,
        'active_tab': 'players'
    })

@login_required
def admin_characters(request):
    """Управление персонажами"""
    search_query = request.GET.get('search', '')
    page = request.GET.get('page', 1)

    characters = Character.objects.select_related('player').all()

    if search_query:
        characters = characters.filter(
            Q(name__icontains=search_query) |
            Q(player__telegram_username__icontains=search_query) |
            Q(player__telegram_id__icontains=search_query)
        )

    paginator = Paginator(characters.order_by('-id'), 20)
    characters_page = paginator.get_page(page)

    return render(request, 'admin_panel/characters.html', {
        'characters': characters_page,
        'search_query': search_query,
        'active_tab': 'characters'
    })

@login_required
def admin_character_detail(request, character_id):
    """Детальная информация о персонаже"""
    character = get_object_or_404(Character.objects.select_related('player', 'stats'), id=character_id)
    equipment = character.player.equipment if hasattr(character.player, 'equipment') else None

    return render(request, 'admin_panel/character_detail.html', {
        'character': character,
        'stats': character.stats if hasattr(character, 'stats') else None,
        'equipment': equipment,
        'active_tab': 'characters'
    })

@login_required
def admin_items(request):
    """Управление предметами"""
    try:
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
        types = Item.ITEM_TYPES

        return render(request, 'admin_panel/items.html', {
            'items': items_page,
            'search_query': search_query,
            'rarity_filter': rarity_filter,
            'type_filter': type_filter,
            'rarities': rarities,
            'types': types,
            'active_tab': 'items'
        })
    except Exception as e:
        # Возвращаем пустые данные в случае ошибки
        return render(request, 'admin_panel/items.html', {
            'items': [],
            'search_query': '',
            'rarity_filter': '',
            'type_filter': '',
            'rarities': [],
            'types': [],
            'active_tab': 'items',
            'error': str(e)
        })

@login_required
def admin_item_detail(request, item_id):
    """Детальная информация о предмете"""
    item = get_object_or_404(Item, id=item_id)

    return render(request, 'admin_panel/item_detail.html', {
        'item': item,
        'active_tab': 'items'
    })

@login_required
@csrf_exempt
def admin_item_create(request):
    """Создание нового предмета"""
    # Отладочная информация
    print(f"User: {request.user}, Is authenticated: {request.user.is_authenticated}")

    try:
        if request.method == 'POST':
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

            is_craftable = request.POST.get('is_craftable') == 'on'

            # Валидация обязательных полей
            if not all([name, description, rarity, item_type]):
                messages.error(request, 'Пожалуйста, заполните все обязательные поля!')
                return redirect('admin_panel:admin_item_create')

            # Создаем базовый предмет
            item = Item.objects.create(
                name=name,
                description=description,
                item_type=item_type,
                cost=value
            )

            # Создаем дополнительные данные в зависимости от типа предмета
            if item_type == 'equipment':
                # Создаем экипировку
                EquipmentItems.objects.create(
                    item=item,
                    equipment_slot=equipment_slot,
                    rarity=rarity,
                    strength_bonus=strength_bonus,
                    agility_bonus=agility_bonus,
                    vitality_bonus=vitality_bonus,
                    attack_bonus=attack_bonus,
                    defense_bonus=defense_bonus,
                    health_bonus=health_bonus,
                    crit_chance_bonus=crit_chance_bonus,
                    dodge_chance_bonus=dodge_chance_bonus,
                    level_requirement=int(request.POST.get('level_requirement', 1))
                )
            elif item_type == 'craft':
                # Создаем предмет крафта
                CraftItems.objects.create(
                    item=item,
                    stack_size=int(request.POST.get('stack_size', 1)),
                    is_craftable=True
                )
            elif item_type == 'resource':
                # Создаем ресурс
                CraftItems.objects.create(
                    item=item,
                    stack_size=int(request.POST.get('stack_size', 64)),
                    is_craftable=False
                )

            messages.success(request, f'Предмет "{name}" успешно создан!')
            return redirect('admin_panel:admin_item_detail', item_id=item.id)

        item_types = Item.ITEM_TYPES
        equipment_slots = EquipmentItems.EQUIPMENT_SLOTS
        rarities = EquipmentItems.RARITIES

        return render(request, 'admin_panel/item_create.html', {
            'item_types': item_types,
            'equipment_slots': equipment_slots,
            'rarities': rarities,
            'active_tab': 'items'
        })
    except Exception as e:
        # Возвращаем данные в случае ошибки
        item_types = Item.ITEM_TYPES
        equipment_slots = EquipmentItems.EQUIPMENT_SLOTS
        rarities = EquipmentItems.RARITIES

        return render(request, 'admin_panel/item_create.html', {
            'item_types': item_types,
            'equipment_slots': equipment_slots,
            'rarities': rarities,
            'active_tab': 'items',
            'error': str(e)
        })

@login_required
def admin_inventory(request):
    """Управление инвентарем"""
    search_query = request.GET.get('search', '')
    page = request.GET.get('page', 1)

    inventory = Inventory.objects.select_related('player', 'item').all()

    if search_query:
        inventory = inventory.filter(
            Q(player__telegram_username__icontains=search_query) |
            Q(player__telegram_id__icontains=search_query) |
            Q(item__name__icontains=search_query)
        )

    paginator = Paginator(inventory.order_by('-id'), 20)
    inventory_page = paginator.get_page(page)

    return render(request, 'admin_panel/inventory.html', {
        'inventory': inventory_page,
        'search_query': search_query,
        'active_tab': 'inventory'
    })

@login_required
def admin_equipment(request):
    """Управление экипировкой"""
    try:
        search_query = request.GET.get('search', '')
        page = request.GET.get('page', 1)

        equipment = PlayerEquipment.objects.select_related('player').prefetch_related(
            'weapon_slot', 'head_slot', 'body_slot', 'legs_slot', 'hands_slot', 'feet_slot', 'amulet_slot', 'ring_slot'
        ).all()

        if search_query:
            equipment = equipment.filter(
                Q(player__telegram_username__icontains=search_query) |
                Q(player__telegram_id__icontains=search_query)
            )

        paginator = Paginator(equipment.order_by('-id'), 20)
        equipment_page = paginator.get_page(page)

        return render(request, 'admin_panel/equipment.html', {
            'equipment': equipment_page,
            'search_query': search_query,
            'active_tab': 'equipment'
        })
    except Exception as e:
        # Возвращаем пустые данные в случае ошибки
        return render(request, 'admin_panel/equipment.html', {
            'equipment': [],
            'search_query': '',
            'active_tab': 'equipment',
            'error': str(e)
        })
