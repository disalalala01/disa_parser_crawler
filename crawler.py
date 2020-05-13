#1 ПАРСЕР ОДНОПОТОЧНЫЙ
#2 ЗАМЕР ВРЕМЕНИ
#3 multiproccessing Pool
#4  ЗАМЕР ВРЕМЕНИ
#5 ЭКСПОРТ В CSV

import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from multiprocessing import Pool

def get_html(url):
    """Принимает url
    и возврашяет html код стр
    """
    respo = requests.get(url)# Response
    return respo.text

def get_all_links(html):
    """БЕРЕТ HTML КОД СТРАНИЦЫ
    НАХОДИТ ТАМА TABLE БЕРЕТ ИЗ НЕГО td
    ОТУДА href И ЗАПИХАЕТ ВСЕ ССЫЛКИ
    В links И ВОЗВРАЩЯЕТ СПИСОК С ССЫЛКАМИ
    """
    soup = BeautifulSoup(html, 'lxml')

    #tds = soup.find('table', id='currencies-all').find_all('td', class_='currency-name')
    tds = soup.find_all('td', class_='cmc-table__cell cmc-table__cell--sticky cmc-table__cell--sortable cmc-table__cell--left cmc-table__cell--sort-by__name')

    links = []

    for td in tds:
        a = td.find('a').get('href')# string

        link  = 'https://coinmarketcap.com' + a #/currencies/bitcoin/

        links.append(link)

    return links


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    try:
        name = soup.find('h1').text.strip()
    except:
        name = ''

    try:
        price = soup.find('span', class_='cmc-details-panel-price__price').text.strip()
    except:
        price = ''

    data = {
    'name': name,
    'price': price}

    return data


def write_csv(data):
    with open('coinmarketcap_with_multi.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow( (data['name'], data['price']) )

        print(data['name'], data['price'], 'parsed')

def make_all(url):
    html = get_html(url)
    data = get_page_data(html)
    write_csv(data)


def main():
    start = datetime.now()
    url = 'https://coinmarketcap.com/all/views/all/'

    all_links = get_all_links(get_html(url))

    with Pool(40) as p:
        p.map(make_all, all_links)  #МЕТО МАП ПЕРВЫМ ПРИНИМАЕТ ФУНКЦИЮ ПОТОМ ИТЕРИРУЮМУЮ ПОСЛЕДОВАТЕЛЬНОСТЬ ПРИМЕР СПИСОК КАЖДВЙ ЭЛЕМЕНТ СПИСКА ПЕРЕДАЕТ В ФУНКЦИЮ

    # for index , url in enumerate(all_links):
    #     html = get_html(url)
    #     data = get_page_data(html)
    #     write_csv(data)
    #     print(index)

    end = datetime.now()
    total = end - start
    print(str(total))





if __name__=='__main__':
    main()
