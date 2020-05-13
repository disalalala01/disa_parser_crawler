# План:
# 1. Выяснить колич стр
# 2. Сформировать список url со стр выдачи
# 3. Сбор данных
import requests
from bs4 import BeautifulSoup

def get_html(url):
    respo = requests.get(url)
    return respo.text

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    ads = soup.find('div', class_='rel listHandler').find_all('div', class_='offer-wrapper')

    for ad in ads:
        # title, price, metro , url
        try:
            title = ad.find('strong')
        except:
            title = ''
        try:
            url = ad.find('a' class_='marginright5 link linkWithHash detailsLink')

def get_total_pages(html):
    """Принимает html код стр
    и выяснить колич стр
    """
    soup = BeautifulSoup(html, 'lxml')

    pages = soup.find('div', class_='pager rel clr').find_all('a', class_='block br3 brc8 large tdnone lheight24')[-1].get('href')

    total_pages = pages.split('?')[1].split('=')[1]

    return int(total_pages)
def  main():
    url = 'https://www.olx.kz/list/q-iphone-11/?page=25'
    base_url ='https://www.olx.kz/'
    page_part = '?page='
    query_part = 'list/q-iphone-11/'

    total_pages = get_total_pages(get_html(url))

    for i in range(1, 3):
        url_gen = base_url + query_part + page_part + str(i)
        # print(url_gen)
        html = get_html(url_gen)
        get_page_data(html)


if __name__=='__main__':
    main()
