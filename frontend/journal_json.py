''' Archivo con todas las funciones que interactuan con archivos json '''

import json, os
from journal import Journal

json_filename = 'revista.json'

def load_json(path: str) -> dict:
    ''' Carga un archivo json '''
    with open(path, 'r', encoding='utf8') as f:
        return json.load(f)

def save_json(data: dict, path: str):
    ''' Guarda diccionario como archivo json '''
    with open(path, 'w', encoding='utf8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def find_common_journals(unison_data: dict, scimago_data: dict) -> dict:
    ''' Crea un nuevo diccionario con solo las revistas que existen en ambos json '''
    common_titles = set(unison_data.keys()) & set(scimago_data.keys())
    combined = {}
    for idx, title in enumerate(sorted(common_titles)):
        combined[title] = {
            'id': str(idx),
            **unison_data[title],
            **scimago_data[title]
        }
    return combined

def create_journal_json(dir_json: str, unison_json: str, scimago_json: str):
    ''' Combina los datos de Unison y Scimago en un solo json '''
    path_unison = os.path.join(dir_json, unison_json)
    path_scimago = os.path.join(dir_json, scimago_json)
    output_path = os.path.join(dir_json, json_filename)

    unison_data = load_json(path_unison)
    scimago_data = load_json(path_scimago)

    combined_data = find_common_journals(unison_data, scimago_data)

    save_json(combined_data, output_path)
    print(f"Archivo json generado.")

def create_journal_dict(path: str) -> dict:
    ''' Crea un diccionario de objetos Journal con ID numérico como clave y atributo '''
    path = os.path.join(path, json_filename)
    journal_json = load_json(path)

    journal_dict = {}
    for idx, (title, info) in enumerate(sorted(journal_json.items())):
        id_str = str(idx)
        journal = Journal(
            id=id_str,
            title=title,
            areas=info.get('areas', []),
            catalogs=info.get('catalogos', []),
            website=info.get('sitio_web', ''),
            h_index=info.get('h_index', ''),
            area_categoria=info.get('area_categoria', []),
            publisher=info.get('publisher', ''),
            issn=info.get('issn', ''),
            widget=info.get('widget', ''),
            publication_type=info.get('publication_type', '')
        )
        journal_dict[id_str] = journal

    return journal_dict