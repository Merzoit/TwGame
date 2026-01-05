import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twgame.settings')
import django
django.setup()

from django.test import Client
from django.contrib.auth import authenticate

def test_admin_access():
    client = Client()

    # Логинимся
    user = authenticate(username='admin', password='admin123')
    if user:
        client.force_login(user)
        print("✓ User authenticated")

        # Проверяем GET страницу создания предметов
        response = client.get('/db-admin/items/create/')
        print(f"GET /db-admin/items/create/: {response.status_code}")

        # Проверяем POST
        response = client.post('/db-admin/items/create/', {
            'name': 'Test Sword',
            'description': 'A test sword',
            'rarity': 'gray',
            'item_type': 'weapon',
            'equipment_slot': 'weapon',
            'value': 10,
            'is_craftable': False
        })
        print(f"POST /db-admin/items/create/: {response.status_code}")

        if response.status_code == 302:
            print(f"Redirect to: {response.url}")
        elif 'CSRF' in str(response.content):
            print("❌ CSRF error detected")
        else:
            print("Response content:", response.content.decode()[:200])
    else:
        print("❌ Authentication failed")

if __name__ == '__main__':
    test_admin_access()

