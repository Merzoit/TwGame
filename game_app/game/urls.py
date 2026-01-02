from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.home, name='home'),
    path('api/status/', views.api_status, name='api_status'),
    path('api/telegram/webhook/', views.telegram_webhook, name='telegram_webhook'),
]
