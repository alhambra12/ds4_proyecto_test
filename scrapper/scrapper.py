from bs4 import BeautifulSoup
import Levenshtein
import requests

class Scrapper:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

    def __init__(self, title):
        self.title = title
        self.url = None
        self.soup = None

    def scrap(self, url):
        page = requests.get(url, headers=Scrapper.headers, timeout=15)
        if page.status_code != 200:
            raise Exception(f"X Error: {page.status_code} en {url}")
        return page

    def search_url(self):
        search_url = f"https://www.scimagojr.com/journalsearch.php?q={self.title.replace(' ', '+')}"
        try:
            page = self.scrap(search_url)
        except Exception as e:
            print(f"X Error buscando '{self.title}': {e}")
            return None

        soup = BeautifulSoup(page.text, 'html.parser')
        results = []
        for a in soup.select('a[href^="journalsearch.php?q="]'):
            title_result = a.select_one('span.jrnlname')
            if title_result:
                results.append({'href': a['href'], 'title': title_result.text.strip()})

        if not results:
            print(f"X No hay resultados para '{self.title}'")
            return None

        best = max(results, key=lambda x: Levenshtein.ratio(self.title.lower(), x['title'].lower()))
        ratio = Levenshtein.ratio(self.title.lower(), best['title'].lower())
        if ratio < 0.9:
            # print(f"! Similitud baja para '{self.title}' con '{best['title']}' ({ratio:.2f})")
            print(f"X No se pudo encontrar URL para '{self.title}'")
            return None
        # print(f"! Similitud alta para '{self.title}' con '{best['title']}' ({ratio:.2f})")
        self.url = "https://www.scimagojr.com/" + best['href']
        print(f"O URL encontrada para '{self.title}'")
        return self.url

    def load_html(self):
        if not self.url:
            return False
        try:
            page = self.scrap(self.url)
            self.soup = BeautifulSoup(page.text, 'html.parser')
            return True
        except Exception as e:
            print(f"X Error accediendo a '{self.title}': {e}")
            return False

    def get_website(self):
        tag = self.soup.find('a', id='question_journal')
        return tag['href'].strip() if tag else None

    def get_h_index(self):
        return self.get_text('H-Index', 'p', 'hindexnumber')

    def get_area_category(self):
        h2 = self.soup.find('h2', string='Subject Area and Category')
        if not h2:
            return None

        area_category = []
        for ul in h2.find_all_next('ul', style="padding-left:0px"):
            if ul.find_previous_sibling('h2') and ul.find_previous_sibling('h2') != h2:
                break
            area = ul.find('a')
            if area:
                sub_ul = ul.find('ul', class_='treecategory')
                category = [a.text.strip() for a in sub_ul.find_all('a')] if sub_ul else []
                area_category.append({'area': area.text.strip(), 'categorias': category})
        return area_category

    def get_publisher(self):
        return self.get_text('Publisher', 'a')

    def get_issn(self):
        return self.get_text('ISSN', 'p')

    def get_publication_type(self):
        return self.get_text('Publication type', 'p')

    def get_widget(self):
        return f'<iframe src="https://www.scimagojr.com/journalsearch.php?q={self.title.replace(" ", "+")}" width="100%" height="600px" frameborder="0"></iframe>'

    def get_text(self, heading, tag_name, class_=None):
        h = self.soup.find('h2', string=heading)
        if h:
            tag = h.find_next(tag_name, class_=class_) if class_ else h.find_next(tag_name)
            return tag.text.strip() if tag else None
        return None

    def get_data(self):
        if not self.url:
            return None

        if not self.soup and not self.load_html():
            return None

        try:
            data = {
                'sitio_web': self.get_website(),
                'h_index': self.get_h_index(),
                'area_categoria': self.get_area_category(),
                'publisher': self.get_publisher(),
                'issn': self.get_issn(),
                'publication_type': self.get_publication_type(),
                'widget': self.get_widget()
            }

            faltantes = [x for x, y in data.items() if y in (None, [], '')]
            if faltantes:
                print(f"! Datos faltantes para '{self.title}': {', '.join(faltantes)}")
            else:
                print(f"O Datos extraídos correctamente.")

            return data
        except Exception as e:
            print(f"X Error extrayendo datos de '{self.title}': {e}")
            return None