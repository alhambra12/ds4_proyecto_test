import requests
from bs4 import BeautifulSoup

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

scimago_url: str = 'https://www.scimagojr.com'
search_url: str = 'https://www.scimagojr.com/journalsearch.php?q='

def scrap(url):
    ''' Función para obtener la pagina web de internet '''
    page = requests.get(url, headers=headers, timeout=15)
    if page.status_code != 200:
        raise Exception(f"X Error: {page.status_code} en {url}")
    return page

def find_journal_url(journal_title: str):
    '''Función que busca la url de una revista en scimagojr.com '''
    journal_search_url = f"{search_url}{journal_title.replace(' ', '+')}"
    journal_search_page = scrap(journal_search_url)
    soup = BeautifulSoup(journal_search_page.text, 'html.parser')
    first_result = soup.select_one('span.jrnlname')
    journal_url = first_result.find_parent('a')['href'] if first_result else ''
    return f'{scimago_url}/{journal_url}'


def get_h_index(journal_url: str):
    ''' Función para obtener el H-Index de una revista '''
    journal_site = scrap(journal_url)
    soup = BeautifulSoup(journal_site.text, 'html.parser')
    h2 = soup.find('h2', string='H-Index')
    index_tag = h2.find_next_sibling('p', class_='hindexnumber')
    return index_tag.text.strip() 

if __name__ == '__main__':
    journal_name = 'Acta Materialia'
    journal_url = find_journal_url(journal_name)
    index = get_h_index(journal_url)
    print(index)