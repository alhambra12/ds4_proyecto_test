''' Programa generador de JSON '''

import os
import csv
import json
import argparse
    
def get_titles(file: str) -> list:
    ''' Función para obtener los títulos de las revistas '''
    titles = []
    with open(file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row["TITULO:"].strip()
            if title.startswith('"') and title.endswith('"'):
                title = title[1:-1]
            titles.append(title)
    return titles

def create_folder_dic(dir: str) -> dict:
    ''' Funcion para crear diccionario con el titulo como key y el nombre de carpeta en una lista como value '''
    dic = {}
    for file in os.listdir(dir):
        value = os.path.splitext(file)[0]
        titles = get_titles(os.path.join(dir, file))
        for title in titles:
            if title not in dic:
                dic[title] = []
            if value not in dic[title]:
                dic[title].append(value)
    return dic

def create_journal_dic(dic_areas: dict, dic_catalogos: dict) -> dict:
    ''' Función para crear diccionario de revistas con áreas y catálogos '''
    journal = {}
    
    for title, area in dic_areas.items():
        if title not in journal:
            journal[title] = {"areas": [], "catalogos": []}
        journal[title]["areas"] = list(set(journal[title]["areas"] + area))
    
    for title, catalogo in dic_catalogos.items():
        if title not in journal:
            journal[title] = {"areas": [], "catalogos": []}
        journal[title]["catalogos"] = list(set(journal[title]["catalogos"] + catalogo))
    
    return journal

def save_json(dic_revista:dict, dir_json: str):
    with open(dir_json, "w", encoding="utf-8") as f:
        json.dump(dic_revista, f, ensure_ascii=False, indent=2)

def check_dir(dir_json:str) -> bool:
    ''' Función para verificar si ya exite un archivo en la ruta '''
    if os.path.exists(dir_json):
        response = input(f"\nEl archivo en '{dir_json}' ya existe. ¿Deseas eliminarlo? (s/n): ").strip().lower()
        if response == 's':
            os.remove(dir_json)
            print(f"\nArchivo en '{dir_json}' ha sido eliminado.")
            return True
        else:
            return False
    return True

def fix_path(path):
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

def main(dir_datos:str, archivo_json:str):
    ''' Función Principal '''

    dir_areas = fix_path(os.path.join(dir_datos, 'csv','areas'))
    dir_catalogos = fix_path(os.path.join(dir_datos, 'csv', 'catalogos'))
    dir_json = fix_path(os.path.join(dir_datos, 'json', archivo_json))

    if check_dir(dir_json):
        dic_areas = create_folder_dic(dir_areas)
        dic_catalogos = create_folder_dic(dir_catalogos)
        dic_revista = create_journal_dic(dic_areas, dic_catalogos)
        save_json(dic_revista, dir_json)
        print(f"\nArchivo JSON guardado en '{dir_json}'")

    print("\nPrograma finalizado.\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generador JSON de revistas')
    parser.add_argument('--dir_datos', type=str, help='Directorio de datos')
    parser.add_argument('--json_file', type=str, help='Nombre del archivo json generado')
    args = parser.parse_args()
    dir_datos = args.dir_datos or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'datos')
    json_file = args.json_file or 'revistas_unison.json'
    main(dir_datos, json_file)
