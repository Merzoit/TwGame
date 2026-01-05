import os
import re

template_dir = os.path.join(os.path.dirname(__file__), 'game_app', 'admin_panel', 'templates', 'admin_panel')

files_to_fix = [
    'equipment.html',
    'character_detail.html',
    'item_detail.html',
    'item_create.html',
    'characters.html',
    'player_detail.html',
    'players.html'
]

for filename in files_to_fix:
    filepath = os.path.join(template_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Заменяем все URL с game:admin_ на admin_panel:admin_
        updated_content = re.sub(r'game:admin_', 'admin_panel:admin_', content)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        print(f'Fixed {filename}')
    else:
        print(f'File not found: {filename}')

print('All files fixed!')
