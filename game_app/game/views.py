from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
import json

# Create your views here.

@require_GET
def home(request):
    """Главная страница игры"""
    return render(request, 'game/index.html', {
        'game_name': 'TwGame',
        'version': '0.1.0',
    })

@require_GET
def api_status(request):
    """API статус"""
    return JsonResponse({
        'status': 'online',
        'game': 'TwGame',
        'version': '0.1.0',
    })

@csrf_exempt
@require_POST
def telegram_webhook(request):
    """Вебхук для Telegram бота"""
    try:
        data = json.loads(request.body)
        # Здесь будет обработка данных от Telegram
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
