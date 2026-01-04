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
]
