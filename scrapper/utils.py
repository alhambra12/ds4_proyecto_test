import json

def cargar_json(nombre_archivo: str) -> dict:
    with open(nombre_archivo, 'r', encoding='utf8') as f:
        return json.load(f)
    
def crear_lista_titulos(revistas_json) -> list:
    return list(revistas_json.keys())