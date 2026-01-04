from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Создаем роутер для ViewSets
router = DefaultRouter()
router.register(r'players', views.PlayerViewSet)
router.register(r'characters', views.CharacterViewSet)
router.register(r'items', views.ItemViewSet)
router.register(r'inventory', views.InventoryViewSet)
router.register(r'equipment', views.EquipmentViewSet)
router.register(r'game', views.GameViewSet, basename='game')

urlpatterns = [
    path('', include(router.urls)),
    # Дополнительные API endpoints
    path('status/', views.api_status, name='api_status'),
]
