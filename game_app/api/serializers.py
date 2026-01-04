from rest_framework import serializers
from accounts.models import Player, PlayerProfile
from characters.models import Character, Equipment
from items.models import Item, Inventory


class PlayerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerProfile
        fields = ['level', 'experience', 'gold', 'total_games', 'wins', 'losses', 'win_rate', 'last_login']


class PlayerSerializer(serializers.ModelSerializer):
    profile = PlayerProfileSerializer(read_only=True)

    class Meta:
        model = Player
        fields = [
            'id', 'telegram_id', 'username', 'first_name', 'last_name',
            'twitch_username', 'twitch_connected', 'is_active', 'created_at', 'profile'
        ]
        read_only_fields = ['id', 'created_at']


class CharacterSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source='player.first_name', read_only=True)

    class Meta:
        model = Character
        fields = [
            'id', 'player', 'player_name', 'name', 'strength', 'agility', 'vitality',
            'free_skill_points', 'level', 'experience', 'max_health', 'current_health',
            'min_attack', 'max_attack', 'defense', 'crit_chance', 'dodge_chance',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


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


class EquipmentSerializer(serializers.ModelSerializer):
    character_name = serializers.CharField(source='character.name', read_only=True)
    item = ItemSerializer(read_only=True)

    class Meta:
        model = Equipment
        fields = ['id', 'character', 'character_name', 'slot', 'item', 'equipped_at']
        read_only_fields = ['id', 'equipped_at']
