from django.contrib import admin
from .models import Player, PlayerStats


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'telegram_username', 'twitch_username', 'twitch_connected', 'last_login', 'created_at']
    list_filter = ['twitch_connected', 'created_at', 'last_login']
    search_fields = ['telegram_id', 'telegram_username', 'twitch_username']
    readonly_fields = ['telegram_id', 'created_at', 'updated_at', 'last_login']
    ordering = ['-created_at']


@admin.register(PlayerStats)
class PlayerStatsAdmin(admin.ModelAdmin):
    list_display = ['player', 'total_matches', 'wins', 'gold', 'diamonds', 'win_rate']
    list_filter = ['total_matches', 'wins']
    search_fields = ['player__telegram_username', 'player__telegram_id']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-total_matches', '-wins']

    def win_rate(self, obj):
        return f"{obj.win_rate}%"
    win_rate.short_description = "Процент побед"
