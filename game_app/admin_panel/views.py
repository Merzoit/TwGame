from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

from accounts.models import Player, PlayerProfile
from characters.models import Character, Equipment
from items.models import Item, Inventory

from accounts.services import PlayerService

# Admin Panel Views

def admin_dashboard(request):
    """Главная страница админ панели"""
    stats = {
        'players_count': Player.objects.count(),
        'characters_count': Character.objects.count(),
        'items_count': Item.objects.count(),
        'inventory_count': Inventory.objects.count(),
    }

    return render(request, 'admin_panel/dashboard.html', {
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

    return render(request, 'admin_panel/players.html', {
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

    return render(request, 'admin_panel/player_detail.html', {
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

    return render(request, 'admin_panel/characters.html', {
        'characters': characters_page,
        'search_query': search_query,
        'active_tab': 'characters'
    })

def admin_character_detail(request, character_id):
    """Детальная информация о персонаже"""
    character = get_object_or_404(Character, id=character_id)
    equipment = PlayerService.get_character_equipment(character)

    return render(request, 'admin_panel/character_detail.html', {
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

    return render(request, 'admin_panel/items.html', {
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

    return render(request, 'admin_panel/item_detail.html', {
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
                return redirect('admin_panel:admin_item_create')

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
            return redirect('admin_panel:admin_item_detail', item_id=item.id)

        except Exception as e:
            messages.error(request, f'Ошибка при создании предмета: {str(e)}')
            return redirect('admin_panel:admin_item_create')

    rarities = Item.RARITIES
    types = Item.TYPES

    return render(request, 'admin_panel/item_create.html', {
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

    return render(request, 'admin_panel/inventory.html', {
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

    return render(request, 'admin_panel/equipment.html', {
        'equipment': equipment_page,
        'search_query': search_query,
        'active_tab': 'equipment'
    })
