''' Programa scrapper de scimagojr.com '''

import os
import argparse
from utils import cargar_json, crear_lista_titulos

def main(dir_json:str, json_entrada:str, json_salida:str):
    ''' Función principal del scrapper de scimagojr.com '''
    
    ruta_entrada = os.path.join(dir_json, json_entrada)
    ruta_salida = os.path.join(dir_json, json_salida)

    revistas_json = cargar_json(ruta_entrada)
    lista_titulos = crear_lista_titulos(revistas_json)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrapper para scimagojr.com')
    parser.add_argument('--dir_json', type=str, help='Directorio de JSONs')
    parser.add_argument('--json_entrada', type=str, help='Nombre del archivo de entrada')
    parser.add_argument('--json_salida', type=str, help='Nombre del archivo de salida')
    args = parser.parse_args()
    dir_json = args.dir_json
    json_entrada = args.json_entrada
    json_salida = args.json_salida
    if not dir_json:
        archivo_entrada = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'datos', 'json')
    if not json_entrada:
        json_entrada = 'revistas.json'
    if not json_salida:
        json_salida = 'scrap.json'
    main(dir_json, json_entrada, json_salida)   