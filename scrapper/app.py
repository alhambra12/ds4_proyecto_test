''' Programa scrapper para scimagojr.com '''

import os, argparse
from functions import fix_path, check_path, load_json, save_json
from scrapper import Scrapper

def main(dir_json:str, input:str, output:str):
    dir_json = fix_path(dir_json)
    input_path = fix_path(os.path.join(dir_json, input))
    output_path = fix_path(os.path.join(dir_json, output))

    if not check_path(output_path):
        return

    joutnals = load_json(input_path)
    data = {}

    print("\nProcesando revistas:")
    for title in joutnals:
        print(f"\n- Procesando: {title}")
        scrapper = Scrapper(title)
        if scrapper.search_url():
            info = scrapper.get_data()
            if info:
                data[title] = info
            else:
                print(f"X No se pudieron extraer datos para '{title}'")

    save_json(data, output_path)

    print(f"\nDatos guardados en '{output_path}'")
    print("\nPrograma finalizado.\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir_json', type=str, help='Directorio de JSONs')
    parser.add_argument('--input', type=str, help='Archivo de entrada')
    parser.add_argument('--output', type=str, help='Archivo de salida')
    args = parser.parse_args()
    dir_json = args.dir_json or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'datos', 'json')
    input = args.input or 'revistas_unison_test.json'
    output = args.output or 'revistas_scimagojr_test.json'

    main(dir_json, input, output)
