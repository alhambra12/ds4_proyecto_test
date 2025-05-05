import json
import random
import os

def load_json(path):
    with open(path, 'r', encoding='utf8') as f:
        return json.load(f)

def save_json(data, path):
    with open(path, 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_journals(journals, cantidad=400):
    keys = list(journals.keys())
    selected = random.sample(keys, cantidad)
    return {k: journals[k] for k in selected}

if __name__ == '__main__':
    journals_dic = load_json(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'datos', 'json', 'revistas_unison.json'))
    selected_journal = get_journals(journals_dic)
    save_json(selected_journal, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'datos', 'json', 'revistas_unison_test.json'))