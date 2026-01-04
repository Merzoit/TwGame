from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('players/', views.admin_players, name='admin_players'),
    path('players/<int:player_id>/', views.admin_player_detail, name='admin_player_detail'),
    path('characters/', views.admin_characters, name='admin_characters'),
    path('characters/<int:character_id>/', views.admin_character_detail, name='admin_character_detail'),
    path('items/', views.admin_items, name='admin_items'),
    path('items/<int:item_id>/', views.admin_item_detail, name='admin_item_detail'),
    path('items/create/', views.admin_item_create, name='admin_item_create'),
    path('inventory/', views.admin_inventory, name='admin_inventory'),
    path('equipment/', views.admin_equipment, name='admin_equipment'),
]
