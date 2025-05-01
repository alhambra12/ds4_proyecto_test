import os
import json

class Utilities:

    @staticmethod
    def load_json(path):
        with open(path, 'r', encoding='utf8') as f:
            return json.load(f)

    @staticmethod
    def save_json(data, path):
        with open(path, 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def check_path(path):
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

    @staticmethod
    def fix_path(path):
        path = path.replace('\\', '/')
        parts = path.split('/')
        resolved = []
        for part in parts:
            if part == '..':
                if resolved:
                    resolved.pop()
            elif part and part != '.':
                resolved.append(part)
        return '/'.join(resolved)
