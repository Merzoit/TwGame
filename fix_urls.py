import os
import re

template_dir = 'game_app/admin_panel/templates/admin_panel'

for filename in os.listdir(template_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(template_dir, filename)

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Заменяем все URL с game:admin_ на admin_panel:admin_
        updated_content = re.sub(r'game:admin_', 'admin_panel:admin_', content)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        print(f'Updated {filename}')


