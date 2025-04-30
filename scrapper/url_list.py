import Levenshtein
import requests
from utils import scrap
from bs4 import BeautifulSoup

def crear_url_busqueda(nombre_revista: str) -> str:
    ''' Función para crear la url de busqueda '''
    return f"https://www.scimagojr.com/journalsearch.php?q={nombre_revista.replace(' ', '+')}"

def obtener_lista_resultado(pagina_busqueda: requests.Response) -> list | None:
    ''' Función para obtener los resultados de la busqueda '''
    soup = BeautifulSoup(pagina_busqueda.text, 'html.parser')
    resultado = []
    for enlace in soup.select('a[href^="journalsearch.php?q="]'):
        nombre = enlace.select_one('span.jrnlname')
        if nombre:
            url = enlace['href']
            resultado.append((url, nombre.text.strip()))
    return resultado if resultado else None

def seleccionar_resultado(nombre_revista: str, resultado: list) -> str | None:
    ''' Función para seleccionar el resultado mas parecido a la busqueda realizada '''
    ratio = 0.9
    nombre_revista = nombre_revista.lower()
    mejor = max(resultado, key=lambda x: Levenshtein.ratio(nombre_revista, x[1].lower()))
    similitud = Levenshtein.ratio(nombre_revista, mejor[1].lower())
    if similitud < ratio:
        print(f"X La mejor coincidencia para '{nombre_revista}' es '{mejor[1]}' pero tiene baja similitud ({similitud:.2f}).")
        return None
    print(f"O La mejor coincidencia para '{nombre_revista}' es '{mejor[1]}' (similitud {similitud:.2f}).")
    return mejor[0]

def encontrar_url_revista(nombre_revista: str) -> str | None:
    ''' Función para encontrar la url de una revista en el sitio simagojr.com '''
    url_busqueda = crear_url_busqueda(nombre_revista)
    try:
        pagina_busqueda = scrap(url_busqueda)
    except Exception as e:
        print(f"X Error al buscar {nombre_revista}: {e}")
        return None
    resultado_lista = obtener_lista_resultado(pagina_busqueda)
    if resultado_lista is None:
        print(f"X No se encontraron resultados para {nombre_revista}")
        return None
    url_relativa = seleccionar_resultado(nombre_revista, resultado_lista)
    if url_relativa is None:
        return None
    return "https://www.scimagojr.com/" + url_relativa

def crear_lista_url(lista_revistas: list) -> list:
    ''' Función para crar lista de tuplas de las url '''
    print('\nObteniendo URLs de las revistas:\n')
    lista_url = []
    for revista in lista_revistas:
        url = encontrar_url_revista(revista)
        if url:
            lista_url.append((revista, url))
    return lista_url
