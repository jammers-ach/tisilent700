# Parser for the restaurant page from launaat.info

import datetime
import dateutil.parser
import requests

from bs4 import BeautifulSoup

def get_menu(url, ourday):
    '''Gets the lunch page for today from a lounaat.info restaurant page'''
    resp = requests.get(url)
    pagetext = resp.text
    soup = BeautifulSoup(pagetext, 'html.parser')
    lunchmenu = soup.find('div', {'id':'menu'})

    name = soup.find('h2',{'itemprop':'name'}).get_text().strip()
    menu = []
    for item in lunchmenu.find_all('div', {'class':'item'}):
        header = item.find('h3')
        if not header:
            continue
        title = header.get_text()
        _, date = title.split()
        day, month, _ = date.split('.')

        if int(day) != ourday.day or int(month) != ourday.month:
            continue

        for food in item.find_all('li'):
            text = food.get_text().strip()
            if text != '':
                menu.append(text)

    if menu == []:
        raise Exception("No menu found")

    return {'name': name,
            'food': menu}

if __name__ == '__main__':
    DEFAULT_URL='https://www.lounaat.info/lounas/amica-lets-play/espoo'
    print(get_menu(DEFAULT_URL, datetime.date.today() + datetime.timedelta(days=-2)))
