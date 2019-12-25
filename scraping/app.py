import requests
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

class FCvoleiCrawler(object):

    TAG_RE = re.compile(r'<[^>]+>')

    def __init__(self, starting_url):
        self.starting_url = starting_url
        self.links = set()
        self.visited = set()


    def get_html(self, url):
        try:
            html = requests.get(url)
        except Exception as e:
            print(e)
            return ""
        return html.content.decode('latin-1')

    def get_links(self, url):
        html = self.get_html(url)
        soup = BeautifulSoup(html, features='html.parser')
        for link in soup.findAll('a', attrs={'href': re.compile("^competiciones")}):
            link = "http://competicio.fcvoleibol.cat/" + link.get('href')
            req = self.get_html(link)
            # get jornadas
            soup = BeautifulSoup(req, features='html.parser')
            jornadas = soup.find_all("option")[-1].get_text()
            for jornada in range(int(jornadas)):
                links = link + "&jornada="+str(jornada)
                self.links.add(links)


        return (self.links)

    def remove_tags(self, text):
        return self.TAG_RE.sub('', text)

    def get_info(self, url):
        req = self.get_html(url)
        noJornada = ['no data','no data','no data','no data','no data']
        data = []

        soup = BeautifulSoup(req, features='html.parser')

        header = soup.div.h2
        try:
            nombre_liga, categoria, fase, grupo, vuelta = str(header).split('<br/>', 4)
        except:
            data.append(noJornada)

        jornada_box = soup.find("div", attrs={'id':'jornada_numero'})
        try:
            numero_jornada, date = str(jornada_box).split('<br/>', 4)
        except:
            numero_jornada = "Horaris no publicats encara"
            date = "Horaris no publicats encara"

        tabla_box = soup.find('div', attrs={'class':'resultados'})

        rows = tabla_box.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])

        del data[0]
        for element in data:
            if len(element) < 2:
                data.remove(element)
            if len(element) is 3:
                data.append(element)
            if len(element) > 5:
                for data in element:
                    del element[5:]

        '''
        msg = ""

        msg += self.remove_tags(nombre_liga) + '\n'
        msg += self.remove_tags(grupo) + '\n'
        msg += self.remove_tags(numero_jornada) + '\n \n'

        for element in data:
            msg += 'Local: '+ element[0] + '\n'
            msg += 'Visitant: '+ element[1] + '\n'
            msg += 'Día: '+ element[2] + '\n'
            msg += 'Hora: '+ element[3] + '\n'
            msg += 'Lloc: '+ element[4] + '\n \n'
        '''
        dataend = []

        for element in data:
            dataend.append(element)
        return dataend

    def crawl(self, url):
        links = self.get_links(url)
        for link in links:
            if link in self.visited:
                continue
            self.visited.add(link)
            data = self.get_info(link)

            print(data)


            self.crawl(link)


    def start(self):
        self.crawl(self.starting_url)

if __name__ == "__main__":
    crawler = FCvoleiCrawler("http://competicio.fcvoleibol.cat/calendaris.asp")
    crawler.start()
