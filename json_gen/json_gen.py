''' Programa generador de JSON '''

import os
import csv
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
        valor = archivo.split()[0]
        titulos = obtener_titulos(os.path.join(dir, archivo))
        for titulo in titulos:
            if titulo not in dic:
                dic[titulo] = []
            if valor not in dic[titulo]:
                dic[titulo].append(valor)
    return dic


def main(dir_csv:str, dir_json:str, archivo_json:str):
    ''' Función Principal '''
    dir_areas = os.path.join(dir_csv, 'areas')
    dic_areas = crear_dic_carpeta(dir_areas)

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