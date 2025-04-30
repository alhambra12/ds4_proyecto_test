import json
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

def cargar_json(nombre_archivo: str) -> dict:
    with open(nombre_archivo, 'r', encoding='utf8') as f:
        return json.load(f)
    
def crear_lista_titulos(revistas_json) -> list:
    return list(revistas_json.keys())

def scrap(url: str) -> requests.Response:
    pagina = requests.get(url, headers=headers, timeout=15)
    if pagina.status_code != 200:
        raise Exception(f'Error {pagina.status_code} en {url}')
    return pagina

def guardar_json(data: dict, archivo_salida: str):
    with open(archivo_salida, 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)