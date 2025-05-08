import os, argparse
from flask import Flask, render_template, abort, request
from functions import get_attribute, create_journal_json, load_journals, get_authors

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
def journal(id_journal):
    ''' Página de detalles de la revista '''
    journal = next((j for j in journals if j.id == id_journal), None)
    if not journal:
        abort(404)
    return render_template('journal.html', journal=journal.to_dict())

@app.route('/areas')
def areas():
    areas = get_attribute(journals, 'areas')
    return render_template('areas.html', areas=areas)

@app.route('/area/<area>')
def area(area):
    journals_by_area = [j for j in journals if area in j.areas]
    return render_template('area.html', area=area, journals=journals_by_area)

@app.route('/catalogos')
def catalogs():
    catalogs = get_attribute(journals, 'catalogs')
    return render_template('catalogs.html', catalogs=catalogs)

@app.route('/catalogo/<catalog>')
def catalog(catalog):
    journals_by_catalog = [j for j in journals if catalog in j.catalogs]
    return render_template('catalog.html', catalog=catalog, journals=journals_by_catalog)

@app.route('/explorar')
def explore():
    return render_template('explore.html', selected_letter=None, journals=[])

@app.route('/explorar/<letter>')
def letter(letter):
    filtered = [j for j in journals if j.title.upper().startswith(letter.upper())]
    return render_template('explore.html', selected_letter=letter.upper(), journals=filtered)

@app.route('/busqueda', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        texto = request.form['titulo'].lower()
        revistas_filtradas = [j for j in journals if texto in j.title.lower()]
        return render_template('search.html', revistas=revistas_filtradas)
    return render_template('search.html')

@app.route('/creditos')
def credits():
    authors = get_authors()
    return render_template('credits.html', authors=authors)

if __name__ == '__main__':
    app.run(debug=True)