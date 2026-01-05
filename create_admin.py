#!/usr/bin/env python3
"""
Script to create admin user for Railway deployment
Run this if superuser creation failed during deployment
"""

import os
import sys
import django

# Add the game_app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'game_app'))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twgame.settings')

# Setup Django
django.setup()

from django.contrib.auth.models import User

def create_admin():
    username = 'admin'
    password = 'admin123'
    email = 'admin@twgame.com'

    try:
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            print(f"✅ Admin user '{username}' password updated")
        else:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            print(f"✅ Admin user '{username}' created")

        # Verify login works
        from django.contrib.auth import authenticate
        user = authenticate(username=username, password=password)
        if user and user.is_superuser:
            print("✅ Admin login verification successful")
        else:
            print("❌ Admin login verification failed")

    except Exception as e:
        print(f"❌ Error creating admin user: {e}")

if __name__ == '__main__':
    create_admin()

