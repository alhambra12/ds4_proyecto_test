import os, argparse
from flask import Flask, render_template, abort
from journal_json import create_journal_json, load_journals
from functions import get_attribute, journals_by_letter

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

journals = load_journals(dir_json)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/revista/<id_journal>')
def journal_view(id_journal):
    ''' Página de detalles de la revista '''
    journal = next((j for j in journals if j.id == id_journal), None)
    if not journal:
        abort(404)
    return render_template('journal.html', journal=journal.to_dict())

@app.route('/areas')
def areas_view():
    areas = get_attribute(journals, 'areas')
    return render_template('areas.html', areas=areas)

@app.route('/areas/<area>')
def area_view(area):
    journals_by_area = [j for j in journals if area in j.areas]
    return render_template('area.html', area=area, journals=journals_by_area)

@app.route('/catalogos')
def catalogs_view():
    catalogs = get_attribute(journals, 'catalogs')
    return render_template('catalogs.html', catalogs=catalogs)

@app.route('/catalogos/<catalog>')
def catalog_view(catalog):
    journals_by_catalog = [j for j in journals if catalog in j.catalogs]
    return render_template('catalog.html', catalog=catalog, journals=journals_by_catalog)

@app.route('/explorar')
def explore_view():
    grouped_journals = journals_by_letter(journals)
    return render_template('explore.html', grouped_journals=grouped_journals)

@app.route('/explorar/<letter>')
def letter_view(letter):
    journals_by_letter = [j for j in journals if j.title and j.title[0].upper() == letter.upper()]
    return render_template('letter.html', letter=letter.upper(), journals=journals_by_letter)

if __name__ == '__main__':
    app.run(debug=True)