import json, os
from journal import Journal

def get_attribute(journals: list, attribute: str) -> list:
    ''' Obtiene valores de un atributo '''
    raw_values = (getattr(j, attribute, None) for j in journals if getattr(j, attribute, None) is not None)
    flattened = [item for val in raw_values for item in (val if isinstance(val, list) else [val])]
    return sorted(set(flattened))

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
    output_path = os.path.join(dir_json, json_filename)

    if os.path.exists(output_path):
        return
    
    path_unison = os.path.join(dir_json, unison_json)
    path_scimago = os.path.join(dir_json, scimago_json)

    unison_data = load_json(path_unison)
    scimago_data = load_json(path_scimago)

    combined_data = find_common_journals(unison_data, scimago_data)

    save_json(combined_data, output_path)
    print(f"Archivo json generado.")

def load_journals(path: str) -> list:
    ''' Crea una lista con la clase Journal '''
    path = os.path.join(path, json_filename)
    journal_json = load_json(path)

    journals = []
    for idx, (title, info) in enumerate(sorted(journal_json.items())):
        journal = Journal(
            id=str(idx),
            title=title,
            areas=info.get('areas', []),
            catalogs=info.get('catalogs', []),
            website=info.get('website', ''),
            h_index=info.get('h_index', ''),
            subjet_area_and_category=info.get('subjet_area_and_category', []),
            publisher=info.get('publisher', ''),
            issn=info.get('issn', ''),
            widget=info.get('widget', ''),
            publication_type=info.get('publication_type', '')
        )
        journals.append(journal)

    return journals

def get_authors():
    return [
        'Pedro Alan Escobedo Salazar',
        'Alejandro Leyva',
        'Alex Pacheco'
        ]