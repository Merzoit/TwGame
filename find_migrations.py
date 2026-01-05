import os
import glob

# Найдем все файлы миграций
migration_files = glob.glob('*/migrations/*.py', recursive=True)

for file_path in migration_files:
    if '__init__.py' not in file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if '\x00' in content:  # null byte
                    print(f'Corrupted file: {file_path}')
                else:
                    print(f'OK: {file_path}')
        except Exception as e:
            print(f'Error reading {file_path}: {e}')


