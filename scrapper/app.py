import os
import argparse
from utilities import Utilities
from scrapper import Scrapper

class Main:
    def __init__(self, dir_json, input, output):
        self.dir = dir_json
        self.input_path = os.path.join(dir_json, input)
        self.output_path = os.path.join(dir_json, output)

    def main(self):
        if not Utilities.check_path(self.output_path):
            return

        magazines = Utilities.load_json(self.input_path)
        data = {}

        print("\nProcesando revistas:")
        for title in magazines:
            print(f"\n- Procesando: {title}")
            scrapper = Scrapper(title)
            if scrapper.search_url():
                info = scrapper.get_data()
                if info:
                    data[title] = info
                else:
                    print(f"X No se pudieron extraer datos para '{title}'")

        Utilities.load_json(data, self.output_path)
        print(f"\nDatos guardados en '{self.output_path}'")
        print("\nPrograma finalizado.\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir_json', type=str, help='Directorio de JSONs')
    parser.add_argument('--input_path', type=str, help='Archivo de entrada')
    parser.add_argument('--output_path', type=str, help='Archivo de salida')
    args = parser.parse_args()

    dir_json = args.dir_json or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'datos', 'json')
    input_path = args.input_path or 'revistas.json'
    output_path = args.output_path or 'scrap.json'

    scraper = Main(dir_json, input_path, output_path)
    scraper.main()
