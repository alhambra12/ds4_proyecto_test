''' Archivo de funciones '''

import os, json

def load_json(path: str):
    with open(path, 'r', encoding='utf8') as f:
        return json.load(f)

def save_json(data, path: str):
    with open(path, 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def check_path(path: str) -> bool:
    if os.path.exists(path):
        response = input(f"\nEl archivo en '{path}' ya existe. ¿Deseas eliminarlo? (s/n): ").strip().lower()
        if response == 's':
            os.remove(path)
            print(f"Archivo en '{path}' eliminado.")
            return True
        else:
            print("\nPrograma finalizado.\n")
            return False
    return True

def fix_path(path: str) -> str:
    path = path.replace('\\', '/')
    parts = path.split('/')
    new_path = []
    for part in parts:
        if part == '..':
            if new_path:
                new_path.pop()
        elif part and part != '.':
            new_path.append(part)
    return '/'.join(new_path)
