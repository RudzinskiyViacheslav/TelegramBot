import requests
from bs4 import BeautifulSoup
#import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import time

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
    ua = UserAgent()
    user_agent = ua.chrome
    AGE_CHECK = True

    options = Options()
    options.add_argument('--window-size=1400,1200')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--disable-extensions")
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument('--enable-javascript')
    options.add_argument('--no-sandbox')
    options.add_argument("--allow-running-insecure-content")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-insecure-localhost')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; "
                         "x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'")
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    chrome_driver = webdriver.Chrome(options=options)
    # chrome_driver.delete_cookie()
    # chrome_driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    time.sleep(5)

    chrome_driver.get(url)
    time.sleep(5)

    try:
        age_confirm_btn = chrome_driver.find_element(By.XPATH,
                                                     "//div[@class='b-button b-button_disabled_false b-button_theme_default b-button_shape_default b-button_size_m b-button_justify_start b-button_selected_false b-offer__alco-action']")
        age_confirm_btn.click()
        #print(age_confirm_btn)
    except Exception as exp:
        AGE_CHECK = False

    vodka_names = chrome_driver.find_elements(By.XPATH, '//div[@class="b-offer__description"]')

    # try:
    #     vodka_names = chrome_driver.find_element(By.CLASS_NAME, "p-offers__header")
    #     print(vodka_names)
    # except Exception as exc:
    #     print(exc)

    vodka_prices_sale = chrome_driver.find_elements(By.XPATH, '//div[@class="b-offer__price-new"]')
    # print(vodka_prices_sale)

    vodka_prices_normal = chrome_driver.find_elements(By.XPATH, '//div[@class="b-offer__price-old"]')
    # print(vodka_prices_normal)

    list_vodkas_to_send_Bot = []

    for i in range(len(vodka_names)):
        list_vodkas_to_send_Bot.append(f'{vodka_names[i].text} нынче по цене {vodka_prices_sale[i].text}, '
                                       f'а была {vodka_prices_normal[i].text}\n')

    str_vodkas_to_send_Bot = '\n'.join(list_vodkas_to_send_Bot)
    # for item in list_vodkas_to_send_Bot:
    #     print(item)

    # for item in vodka_names:
    #     print(item.text)

    chrome_driver.quit()
    if AGE_CHECK:
        str_AGE_CHECK = 'Была проверка на возраст, но я ее обошел!\n'
    else:
        str_AGE_CHECK = 'Даже не было проверки на возраст)\n'

    return str_AGE_CHECK, str_vodkas_to_send_Bot

