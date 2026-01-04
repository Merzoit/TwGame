from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.home, name='home'),
    path('api/status/', views.api_status, name='api_status'),
    path('api/telegram/webhook/', views.telegram_webhook, name='telegram_webhook'),
    path('api/create-character/', views.create_character, name='create_character'),

    # Twitch OAuth
    path('auth/twitch/', views.twitch_auth, name='twitch_auth'),
    path('auth/twitch/callback/', views.twitch_callback, name='twitch_callback'),

    # Equipment API
    path('api/equip-item/', views.equip_item, name='equip_item'),
    path('api/unequip-item/', views.unequip_item, name='unequip_item'),

    # Admin Panel
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/players/', views.admin_players, name='admin_players'),
    path('admin/players/<int:player_id>/', views.admin_player_detail, name='admin_player_detail'),
    path('admin/characters/', views.admin_characters, name='admin_characters'),
    path('admin/characters/<int:character_id>/', views.admin_character_detail, name='admin_character_detail'),
    path('admin/items/', views.admin_items, name='admin_items'),
    path('admin/items/<int:item_id>/', views.admin_item_detail, name='admin_item_detail'),
    path('admin/items/create/', views.admin_item_create, name='admin_item_create'),
    path('admin/inventory/', views.admin_inventory, name='admin_inventory'),
    path('admin/equipment/', views.admin_equipment, name='admin_equipment'),
]
