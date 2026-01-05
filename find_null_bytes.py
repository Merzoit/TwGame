import os

def find_null_bytes_files(directory):
    """Найти файлы с null bytes"""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'rb') as f:
                        content = f.read()
                        if b'\x00' in content:
                            print(f'Found null bytes in: {filepath}')
                except Exception as e:
                    print(f'Error reading {filepath}: {e}')

if __name__ == '__main__':
    find_null_bytes_files('.')
    print('Scan complete!')


