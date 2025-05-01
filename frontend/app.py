''' Programa front end '''

import argparse, os
from flask import Flask, render_template

app = Flask(__name__)

dir_json = None
unison_json = None
scimago_json = None

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir_json', type=str, help='Directorio de JSONs')
    parser.add_argument('--unison_json', type=str, help='Archivo de json con los datos de la universidad')
    parser.add_argument('--scimago_json', type=str, help='Archivo de json con los datos de scimagojr')
    args = parser.parse_args()
    dir_json = args.dir_json or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'datos', 'json')
    unison_json = args.unison_json or 'revistas_test.json'
    scimago_json = args.scimago_json or 'scrap_test.json'

    app.run(debug=True)