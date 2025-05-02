from collections import defaultdict

def get_attribute(journals: list, attribute: str) -> list:
    ''' Obtiene valores de un atributo '''
    raw_values = (getattr(j, attribute, None) for j in journals if getattr(j, attribute, None) is not None)
    flattened = [item for val in raw_values for item in (val if isinstance(val, list) else [val])]
    return sorted(set(flattened))

def journals_by_letter(journals: list) -> dict:
    ''' Agrupa revistas por la primera letra del título '''
    grouped = defaultdict(list)
    for j in journals:
        if j.title:  # Verifica que tenga título
            first_letter = j.title[0].upper()
            if first_letter.isalpha():
                grouped[first_letter].append(j)
    return grouped
