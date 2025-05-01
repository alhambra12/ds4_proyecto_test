import json
import random
import os

def load_json(path):
    with open(path, 'r', encoding='utf8') as f:
        return json.load(f)

def save_json(data, path):
    with open(path, 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_magazines(magazines, cantidad=200):
    keys = list(magazines.keys())
    selected = random.sample(keys, cantidad)
    return {k: magazines[k] for k in selected}

if __name__ == '__main__':
    magazines_dic = load_json(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'datos', 'json', 'revistas.json'))
    selected_magazines = get_magazines(magazines_dic, 100)
    save_json(selected_magazines, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'datos', 'json', 'revistas_test.json'))


magazines_dic = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'datos', 'json', 'revistas.json')