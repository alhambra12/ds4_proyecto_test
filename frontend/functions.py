from journal_json import load_journals
import os

def get_attribute(journals: list, attribute: str) -> list:
    ''' Obtiene valores de un atributo '''
    raw_values = (getattr(j, attribute, None) for j in journals if getattr(j, attribute, None) is not None)
    flattened = [item for val in raw_values for item in (val if isinstance(val, list) else [val])]
    return sorted(set(flattened))


dir_json = os.path.join(os.path.dirname(__file__), '..', 'datos', 'json')

journals = load_journals(dir_json)

a = get_attribute(journals, 'catalogs')
print(a)