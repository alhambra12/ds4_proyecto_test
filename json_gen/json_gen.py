''' Programa generador de JSON '''

import os
import argparse

def main(dir_csv:str, dir_json:str, archivo_json:str):
    ''' Función Principal '''

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