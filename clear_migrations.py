import os
import shutil

apps_to_clear = [
    'accounts',
    'characters',
    'core',
    'items',
    'telegram_bot',
    'twitch_integration',
    'admin_panel',
    'api'
]

for app in apps_to_clear:
    migrations_dir = os.path.join(app, 'migrations')

    # Удаляем все файлы кроме __init__.py
    for filename in os.listdir(migrations_dir):
        if filename != '__init__.py':
            filepath = os.path.join(migrations_dir, filename)
            if os.path.isfile(filepath):
                os.remove(filepath)
                print(f'Removed {filepath}')

    # Создаем __init__.py если его нет
    init_file = os.path.join(migrations_dir, '__init__.py')
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write('')
        print(f'Created {init_file}')

print('All migrations cleared!')


