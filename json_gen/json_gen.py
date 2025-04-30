''' Programa generador de JSON '''

import os
import csv
import json
import argparse
    
def obtener_titulos(archivo: str) -> list:
    ''' Función para obtener los títulos de las revistas '''
    titulos = []
    with open(archivo, newline='', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        for fila in lector:
            titulo = fila["TITULO:"].strip()
            if titulo.startswith('"') and titulo.endswith('"'):
                titulo = titulo[1:-1]
            titulos.append(titulo)
    return titulos

def crear_dic_carpeta(dir: str) -> dict:
    ''' Funcion para crear diccionario con el titulo como key y el nombre de carpeta en una lista como value '''
    dic = {}
    for archivo in os.listdir(dir):
        valor = os.path.splitext(archivo)[0]
        titulos = obtener_titulos(os.path.join(dir, archivo))
        for titulo in titulos:
            if titulo not in dic:
                dic[titulo] = []
            if valor not in dic[titulo]:
                dic[titulo].append(valor)
    return dic

def crear_dic_revistas(dic_areas: dict, dic_catalogos: dict) -> dict:
    ''' Función para crear diccionario de revistas con áreas y catálogos '''
    revistas = {}
    
    for titulo, lista in dic_areas.items():
        if titulo not in revistas:
            revistas[titulo] = {"areas": [], "catalogos": []}
        revistas[titulo]["areas"] = list(set(revistas[titulo]["areas"] + lista))
    
    for titulo, lista in dic_catalogos.items():
        if titulo not in revistas:
            revistas[titulo] = {"areas": [], "catalogos": []}
        revistas[titulo]["catalogos"] = list(set(revistas[titulo]["catalogos"] + lista))
    
    return revistas

def guardar_json(dic_revista:dict, dir_json: str):
    with open(dir_json, "w", encoding="utf-8") as f:
        json.dump(dic_revista, f, ensure_ascii=False, indent=2)

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

def main(dir_csv:str, dir_json:str, archivo_json:str):
    ''' Función Principal '''

    # crea rutas
    dir_areas = os.path.join(dir_csv, 'areas')
    dir_catalogos = os.path.join(dir_csv, 'catalogos')
    dir_json =  os.path.join(dir_json, archivo_json)

    if not verificar_dir_json(dir_json):
        return

    # crea diccionarios de area y catalogos
    dic_areas = crear_dic_carpeta(dir_areas)
    dic_catalogos = crear_dic_carpeta(dir_catalogos)

    # crea diccionario de revistas
    dic_revista = crear_dic_revistas(dic_areas, dic_catalogos)
    # exporta a json
    guardar_json(dic_revista, dir_json)
    print(f"\nArchivo JSON guardado en '{dir_json}'")

    print("\nPrograma finalizado.\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrapper para Scimagojr')
    parser.add_argument('--dir_csv', type=str, help='Directorio de csv')
    parser.add_argument('--dir_json', type=str, help='Directorio de json')
    parser.add_argument('--archivo_json', type=str, help='Nombre del archivo json')
    args = parser.parse_args()
    dir_csv = args.dir_csv
    dir_json = args.dir_json
    archivo_json = args.archivo_json
    if not dir_csv:
        dir_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'datos', 'csv')
    if not dir_json:
        dir_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'datos', 'json')
    if not archivo_json:
        archivo_json = 'revistas.json'
    main(dir_csv, dir_json, archivo_json)