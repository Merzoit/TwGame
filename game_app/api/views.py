from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q

from accounts.models import Player, PlayerProfile
from characters.models import Character, Equipment
from items.models import Item, Inventory
from .serializers import (
    PlayerSerializer, PlayerProfileSerializer,
    CharacterSerializer, EquipmentSerializer,
    ItemSerializer, InventorySerializer
)
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def api_status(request):
    """API статус"""
    return Response({'status': 'ok', 'version': '1.0.0'})


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для игроков"""
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def get_queryset(self):
        queryset = Player.objects.select_related('profile').all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(telegram_id__icontains=search)
            )
        return queryset


class CharacterViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для персонажей"""
    queryset = Character.objects.select_related('player').all()
    serializer_class = CharacterSerializer

    def get_queryset(self):
        queryset = Character.objects.select_related('player').all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(player__username__icontains=search) |
                Q(player__first_name__icontains=search)
            )
        return queryset


class ItemViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для предметов"""
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_queryset(self):
        queryset = Item.objects.filter(is_active=True)
        search = self.request.query_params.get('search', None)
        rarity = self.request.query_params.get('rarity', None)
        item_type = self.request.query_params.get('type', None)

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )

        if rarity:
            queryset = queryset.filter(rarity=rarity)

        if item_type:
            queryset = queryset.filter(item_type=item_type)

        return queryset


class InventoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для инвентаря"""
    queryset = Inventory.objects.select_related('player', 'item').all()
    serializer_class = InventorySerializer

    def get_queryset(self):
        queryset = Inventory.objects.select_related('player', 'item').all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(player__username__icontains=search) |
                Q(player__first_name__icontains=search) |
                Q(item__name__icontains=search)
            )
        return queryset


class EquipmentViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для экипировки"""
    queryset = Equipment.objects.select_related('character__player', 'item').all()
    serializer_class = EquipmentSerializer

    def get_queryset(self):
        queryset = Equipment.objects.select_related('character__player', 'item').all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(character__name__icontains=search) |
                Q(character__player__username__icontains=search) |
                Q(character__player__first_name__icontains=search)
            )
        return queryset


# API для игровых действий
class GameViewSet(viewsets.ViewSet):
    """ViewSet для игровых действий"""

    @action(detail=False, methods=['post'])
    def equip_item(self, request):
        """Экипировка предмета"""
        try:
            telegram_id = request.data.get('telegram_id')
            item_id = request.data.get('item_id')
            slot = request.data.get('slot')

            if not all([telegram_id, item_id, slot]):
                return Response({'error': 'Отсутствуют необходимые данные'}, status=status.HTTP_400_BAD_REQUEST)

            # Получаем персонажа
            character = get_object_or_404(Character, player__telegram_id=telegram_id)

            # Получаем предмет из инвентаря
            inventory_item = get_object_or_404(Inventory, player__telegram_id=telegram_id, item_id=item_id)

            # Получаем или создаем слот экипировки
            equipment, created = Equipment.objects.get_or_create(
                character=character,
                slot=slot,
                defaults={'item': inventory_item.item}
            )

            if not created:
                equipment.item = inventory_item.item
                equipment.save()

            # Уменьшаем количество предметов в инвентаре
            inventory_item.quantity -= 1
            if inventory_item.quantity <= 0:
                inventory_item.delete()
            else:
                inventory_item.save()

            # Пересчитываем характеристики персонажа
            character.save()

            return Response({'success': True})

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def unequip_item(self, request):
        """Снятие предмета с экипировки"""
        try:
            telegram_id = request.data.get('telegram_id')
            slot = request.data.get('slot')

            if not all([telegram_id, slot]):
                return Response({'error': 'Отсутствуют необходимые данные'}, status=status.HTTP_400_BAD_REQUEST)

            # Получаем персонажа
            character = get_object_or_404(Character, player__telegram_id=telegram_id)

            # Получаем экипировку
            equipment = get_object_or_404(Equipment, character=character, slot=slot)

            if equipment.item:
                # Добавляем предмет обратно в инвентарь
                inventory, created = Inventory.objects.get_or_create(
                    player=character.player,
                    item=equipment.item,
                    defaults={'quantity': 1}
                )
                if not created:
                    inventory.quantity += 1
                    inventory.save()

                # Снимаем предмет
                equipment.item = None
                equipment.save()

                # Пересчитываем характеристики персонажа
                character.save()

            return Response({'success': True})

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
