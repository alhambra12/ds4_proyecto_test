from flask import Flask, render_template, abort
from journal_json import create_journal_json, create_journal_dict
import os, argparse

app = Flask(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('--dir_json', type=str, help='Directorio de JSONs')
parser.add_argument('--unison_json', type=str, help='Archivo de json con los datos de la universidad')
parser.add_argument('--scimago_json', type=str, help='Archivo de json con los datos de scimagojr')
args = parser.parse_args()

dir_json = args.dir_json or os.path.join(os.path.dirname(__file__), '..', 'datos', 'json')
unison_json = args.unison_json or 'revistas_unison_test.json'
scimago_json = args.scimago_json or 'revistas_scimagojr_test.json'

create_journal_json(dir_json, unison_json, scimago_json)

journals = create_journal_dict(dir_json)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/revista/<id_journal>')
def journal(id_journal):
    ''' Página de detalles de la revista '''
    journal_obj = journals.get(id_journal)
    if not journal_obj:
        abort(404)

    return render_template('journal.html', journal=journal_obj.to_dict())

if __name__ == '__main__':
    app.run(debug=True)