from bs4 import BeautifulSoup
import requests
import re

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)

def get_info(url):
    req = requests.get(url)
    errorjornada = ['no data','no data','no data','no data','no data']

    soup = BeautifulSoup(req.text, 'html.parser')

    header = soup.div.h2
    try:
        nombre_liga, categoria, fase, grupo, vuelta = str(header).split('<br/>', 4)
    except:
        data.append(errorjornada)

    jornada_box = soup.find("div", attrs={'id':'jornada_numero'})
    try:
        numero_jornada, date = str(jornada_box).split('<br/>', 4)
    except:
        numero_jornada = "Horaris no publicats encara"
        date = "Horaris no publicats encara"

    data = []
    tabla_box = soup.find('div', attrs={'class':'resultados'})

    rows = tabla_box.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])

    del data[0]
    dataSQV = []
    for element in data:
        if len(element) > 3:
            if 'SANT QUIRZE' in str(element[0]) or 'SANT QUIRZE' in str(element[1]):
                if len(element) < 1:
                    element.insert(0, 'No data')
                if len(element) < 2:
                    element.insert(1, 'No data')
                if len(element) < 3:
                    element.insert(2, 'No data')
                if len(element) < 4:
                    element.insert(3, 'No data')
                if len(element) < 5:
                    element.insert(4, 'No data')
                dataSQV.append(element)

    msg = ""

    msg += remove_tags(nombre_liga) + '\n'
    msg += remove_tags(grupo) + '\n'
    msg += remove_tags(numero_jornada) + '\n \n'

    for element in dataSQV:
        msg += 'Local: '+ element[0] + '\n'
        msg += 'Visitant: '+ element[1] + '\n'
        msg += 'Día: '+ element[2] + '\n'
        msg += 'Hora: '+ element[3] + '\n'
        msg += 'Lloc: '+ element[4] + '\n \n'

    return msg
