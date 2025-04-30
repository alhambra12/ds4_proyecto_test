import os
import json
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

def cargar_json(nombre_archivo: str) -> dict:
    ''' Función para cargar el json de revistas '''
    with open(nombre_archivo, 'r', encoding='utf8') as f:
        return json.load(f)
    
def crear_lista_titulos(revistas_json) -> list:
    ''' Función para tomar las keys (titulos) y crear una lista '''
    return list(revistas_json.keys())

def scrap(url: str) -> requests.Response:
    ''' Función para obtener una pagina desde internet '''
    pagina = requests.get(url, headers=headers, timeout=15)
    if pagina.status_code != 200:
        raise Exception(f'Error {pagina.status_code} en {url}')
    return pagina

def guardar_json(data: dict, archivo_salida: str):
    ''' Función para guardar en un archivo json '''
    with open(archivo_salida, 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def verificar_dir_json(dir_json:str) -> bool:
    ''' Función para verificar si ya exite un archivo en la ruta '''
    if os.path.exists(dir_json):
        respuesta = input(f"\nEl archivo en '{dir_json}' ya existe. ¿Deseas eliminarlo? (s/n): ").strip().lower()
        if respuesta == 's':
            os.remove(dir_json)
            print(f"\nArchivo en '{dir_json}' ha sido eliminado.")
            return True
        else:
            print("\nPrograma finalizado.\n")
            return False
    return True