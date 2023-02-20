import requests
from bs4 import BeautifulSoup
#import pandas as pd

def get_github_data(url):
    response = requests.get(url)

    content = response.text

    soup = BeautifulSoup(content, 'html.parser')

    info = soup.find('div', class_='Details-content--hidden-not-important '
                                       'js-navigation-container js-active-navigation-container d-md-block')

    info2 = soup.find_all('div', class_='Box-row Box-row--focus-gray py-2 d-flex position-relative js-navigation-item')
    info3 = soup.find_all('div', class_='flex-auto min-width-0 col-md-2 mr-3')


    if response.status_code:
        print(f'Подключение в норме и установлено с кодом {response.status_code}')
    #print(soup)
    # print(type(info2))

    data_from_github_list = []

    for item in info3:
        data_from_github_list.append(item.text.strip())

    data_from_github_str = '\n'.join(data_from_github_list)
    return data_from_github_str
    #print(item.text.strip())

def get_vodka_price_winelab(url):
    response = requests.get(url)
    content = response.text
    soup = BeautifulSoup(content, 'html.parser')

    soup_find = soup.find_all('div', class_=' col-12 col-sm-6 col-md-6 col-lg-4')

    if response.status_code:
        print(f'Подключение в норме и установлено с кодом {response.status_code}')

    vodka_from_winelab_list =[]
    for item in soup_find:
        vodka_from_winelab_list.append(item.text.strip())

    vodka_from_winelab_str = 0



