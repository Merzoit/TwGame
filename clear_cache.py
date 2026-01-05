import shutil
import os

# Удаляем все __pycache__ директории
for root, dirs, files in os.walk('.'):
    for d in dirs:
        if d == '__pycache__':
            shutil.rmtree(os.path.join(root, d))
            print(f'Removed {os.path.join(root, d)}')

# Удаляем все .pyc файлы
for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.pyc'):
            os.remove(os.path.join(root, f))
            print(f'Removed {os.path.join(root, f)}')

print('Cache cleared!')


