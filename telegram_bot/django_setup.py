#!/usr/bin/env python3
"""
Инициализация Django для использования в Telegram боте
"""

import os
import sys
import django

# Добавляем путь к Django проекту
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'game_app'))

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twgame.settings')
django.setup()

print("Django initialized successfully")
