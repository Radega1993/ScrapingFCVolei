import requests
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import sys

from bdsql import PYbd

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
        noJornada = ["No data"] * 5
        data = []
        data_list = []
        soup = BeautifulSoup(req, features='html.parser')

        header = soup.div.h2
        try:
            nombre_liga, categoria, fase, grupo, vuelta = str(header).split('<br/>', 4)
        except:
            nombre_liga = categoria = fase = grupo = vuelta = "No data"

        jornada_box = soup.find("div", attrs={'id':'jornada_numero'})
        try:
            numero_jornada, date = str(jornada_box).split('<br/>', 4)
        except:
            numero_jornada = "Horaris no publicats encara"
            date = "Horaris no publicats encara"

        tabla_box = soup.find('div', attrs={'class':'resultados'})

        if tabla_box is not None:
            rows = tabla_box.find_all('tr')

            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele])

            del data[0]
            for element in data:
                if len(element) < 2:
                    data.remove(element)
                if len(element) > 5:
                    for info in element:
                        del element[5:]

            nom_liga = self.remove_tags(nombre_liga)
            grup = self.remove_tags(grupo)
            num_jornada = self.remove_tags(numero_jornada)

            for element in data:
                try:
                    local = element[0]
                except Exception as e:
                    local = "No data"
                try:
                    visitant = element[1]
                except Exception as e:
                    visitant = "No data"
                try:
                    dia = element[2]
                except Exception as e:
                    dia = "No data"
                try:
                    hora = element[3]
                except Exception as e:
                    hora = "No data"
                try:
                    lugar = element[4]
                except Exception as e:
                    lugar = "No data"


                data = {
                    "nombre_liga":nom_liga,
                    "grupo":grup,
                    "numero_jornada":num_jornada,
                    "local":local,
                    "visitant":visitant,
                    "dia":dia,
                    "hora":hora,
                    "lugar":lugar
                }
                data_list.append(data)
        return data_list


    def crawl(self, url):
        links = self.get_links(url)
        for link in links:
            if link in self.visited:
                continue
            self.visited.add(link)
            data = self.get_info(link)

            bd = PYbd()
            bd.push_data(data)

            #self.crawl(link)


    def start(self):
        self.crawl(self.starting_url)


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    crawler = FCvoleiCrawler("http://competicio.fcvoleibol.cat/calendaris.asp")
    crawler.start()
