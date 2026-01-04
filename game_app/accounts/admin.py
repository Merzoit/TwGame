from django.contrib import admin
from .models import Player, PlayerProfile


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'username', 'first_name', 'last_name', 'twitch_connected', 'is_active', 'created_at']
    list_filter = ['is_active', 'twitch_connected', 'created_at']
    search_fields = ['telegram_id', 'username', 'first_name', 'last_name']
    readonly_fields = ['telegram_id', 'created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(PlayerProfile)
class PlayerProfileAdmin(admin.ModelAdmin):
    list_display = ['player', 'level', 'experience', 'gold', 'win_rate', 'last_login']
    list_filter = ['level', 'last_login']
    search_fields = ['player__username', 'player__first_name', 'player__telegram_id']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-level', '-experience']
