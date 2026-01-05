from rest_framework import serializers
from accounts.models import Player, PlayerStats
from characters.models import Character, CharacterStats
from items.models import Item, Inventory, PlayerEquipment


class PlayerStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerStats
        fields = ['total_matches', 'wins', 'gold', 'diamonds', 'win_rate', 'created_at', 'updated_at']

    def get_win_rate(self, obj):
        return obj.win_rate


class PlayerSerializer(serializers.ModelSerializer):
    stats = PlayerStatsSerializer(read_only=True)

    class Meta:
        model = Player
        fields = [
            'id', 'telegram_id', 'telegram_username', 'twitch_username', 'twitch_id',
            'twitch_connected', 'created_at', 'updated_at', 'last_login', 'stats'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CharacterStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterStats
        fields = [
            'health', 'max_health', 'strength', 'agility', 'vitality',
            'min_attack', 'max_attack', 'defense', 'critical_chance', 'dodge_chance',
            'created_at', 'updated_at'
        ]


class CharacterSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source='player.telegram_username', read_only=True)
    stats = CharacterStatsSerializer(read_only=True)

    class Meta:
        model = Character
        fields = [
            'id', 'player', 'player_name', 'name', 'level', 'experience',
            'created_at', 'updated_at', 'stats'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            'id', 'name', 'description', 'item_type', 'equipment_slot', 'rarity',
            'strength_bonus', 'agility_bonus', 'vitality_bonus', 'attack_bonus',
            'defense_bonus', 'health_bonus', 'crit_chance_bonus', 'dodge_chance_bonus',
            'value', 'stackable', 'max_stack', 'is_equippable', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class InventorySerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    player_name = serializers.CharField(source='player.first_name', read_only=True)

    class Meta:
        model = Inventory
        fields = ['id', 'player', 'player_name', 'item', 'quantity', 'total_value', 'obtained_at']
        read_only_fields = ['id', 'obtained_at', 'total_value']


class PlayerEquipmentSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source='player.telegram_username', read_only=True)
    weapon_slot_name = serializers.CharField(source='weapon_slot.name', read_only=True)
    head_slot_name = serializers.CharField(source='head_slot.name', read_only=True)
    body_slot_name = serializers.CharField(source='body_slot.name', read_only=True)
    legs_slot_name = serializers.CharField(source='legs_slot.name', read_only=True)
    hands_slot_name = serializers.CharField(source='hands_slot.name', read_only=True)
    feet_slot_name = serializers.CharField(source='feet_slot.name', read_only=True)
    amulet_slot_name = serializers.CharField(source='amulet_slot.name', read_only=True)
    ring_slot_name = serializers.CharField(source='ring_slot.name', read_only=True)

    class Meta:
        model = PlayerEquipment
        fields = [
            'id', 'player', 'player_name',
            'weapon_slot', 'weapon_slot_name',
            'head_slot', 'head_slot_name',
            'body_slot', 'body_slot_name',
            'legs_slot', 'legs_slot_name',
            'hands_slot', 'hands_slot_name',
            'feet_slot', 'feet_slot_name',
            'amulet_slot', 'amulet_slot_name',
            'ring_slot', 'ring_slot_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


