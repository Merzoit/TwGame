import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twgame.settings')
import django
django.setup()

from django.test import Client
from django.contrib.auth import authenticate

def test_csrf():
    client = Client()

    # Проверяем GET страницу создания предметов без логина
    response = client.get('/db-admin/items/create/')
    print('GET without login:', response.status_code)

    # Логинимся
    user = authenticate(username='admin', password='admin123')
    if user:
        client.force_login(user)

        # Проверяем GET после логина
        response = client.get('/db-admin/items/create/')
        print('GET with login:', response.status_code)

        # Проверяем POST без CSRF токена (теперь должно работать с @csrf_exempt)
        response = client.post('/db-admin/items/create/', {
            'name': 'Test Item',
            'description': 'Test description',
            'rarity': 'gray',
            'item_type': 'weapon',
            'equipment_slot': 'weapon',
            'value': 10,
            'is_craftable': False
        })
        print('POST without CSRF:', response.status_code)

        if response.status_code == 302:
            print('Success: Item created and redirected')
        else:
            print('Response content:', response.content.decode()[:200])

if __name__ == '__main__':
    test_csrf()
