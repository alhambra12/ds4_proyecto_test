from bs4 import BeautifulSoup
from utils import scrap

def extraer_website(soup):
    enlace = soup.find('a', id='question_journal')
    return enlace['href'].strip() if enlace else None

def extraer_h_index(soup):
    h_index_label = soup.find('h2', string='H-Index')
    if h_index_label:
        h_index = h_index_label.find_next('p', class_='hindexnumber')
        return h_index.text.strip() if h_index else None
    return None

def extraer_area_category(soup):
    area_header = soup.find('h2', string='Subject Area and Category')
    if not area_header:
        return None

    area_categoria = []
    for ul in area_header.find_all_next('ul', style="padding-left:0px"):
        if ul.find_previous_sibling('h2') and ul.find_previous_sibling('h2') != area_header:
            break
        area_info = {}
        area_link = ul.find('a')
        if area_link:
            area_info['area'] = area_link.text.strip()
            sub_ul = ul.find('ul', class_='treecategory')
            if sub_ul:
                cat_links = sub_ul.find_all('a')
                area_info['categorias'] = [a.text.strip() for a in cat_links]
            else:
                area_info['categorias'] = []
            area_categoria.append(area_info)
    return area_categoria if area_categoria else None

def extraer_publisher(soup):
    pub = soup.find('h2', string='Publisher')
    if pub:
        enlace = pub.find_next('a')
        return enlace.text.strip() if enlace else None
    return None

def extraer_issn(soup):
    issn = soup.find('h2', string='ISSN')
    if issn:
        parrafo = issn.find_next('p')
        return parrafo.text.strip() if parrafo else None
    return None

def extraer_publication_type(soup):
    pubtype = soup.find('h2', string='Publication type')
    if pubtype:
        parrafo = pubtype.find_next('p')
        return parrafo.text.strip() if parrafo else None
    return None

def crear_widget(nombre_revista):
    return f'<iframe src="https://www.scimagojr.com/journalsearch.php?q={nombre_revista.replace(" ", "+")}" width="100%" height="600px" frameborder="0"></iframe>'


def extraer_datos(lista_url: list) -> dict:
    ''' Función para obtener los datos de la revista '''
    print('\nExtrayendo datos de las revistas:\n')
    datos = {}
    for nombre_revista, url in lista_url:
        try:
            pagina = scrap(url)
            soup = BeautifulSoup(pagina.text, 'html.parser')

            sitio_web = extraer_website(soup)
            h_index = extraer_h_index(soup)
            area_categoria = extraer_area_category(soup)
            publisher = extraer_publisher(soup)
            issn = extraer_issn(soup)
            publication_type = extraer_publication_type(soup)

            if None in (nombre_revista, sitio_web, h_index, area_categoria, publisher, issn, publication_type):
                print(f"X Datos incompletos para '{nombre_revista}'.")
                continue

            info = {
                'sitio_web': sitio_web,
                'h_index': h_index,
                'area_categoria': area_categoria,
                'publisher': publisher,
                'issn': issn,
                'publication_type': publication_type,
                'widget': crear_widget(nombre_revista)
            }

            datos[nombre_revista] = info
            print(f"O Información extraída exitosamente de '{nombre_revista}'")

        except Exception as e:
            print(f"X Error extrayendo datos de '{nombre_revista}': {e}")
    return datos
