from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs4
import time
import pickle
import os
from settings import dump_info, Manga

mangalib = "https://mangalib.me"
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-ssl-errors')
options.add_argument(f'--disk-cache-dir={os.getcwd()}\cache')
options.add_argument('--headless')

if os.stat('settings').st_size == 0:
    dump_info()

with open('settings', 'rb') as f:
    info = pickle.load(f)

driver = webdriver.Chrome(options=options)

def mangalib_parse():
    driver.get(mangalib + "/login")

    driver.find_element(By.NAME, 'email').send_keys(info[0]['email'])
    driver.find_element(By.NAME, 'password').send_keys(info[0]['password'])
    driver.find_element(By.XPATH, '//button').click()

    if info[0]['id'] == "": 
        bs = bs4(driver.page_source, 'html.parser')
        id_ = bs.find_all('img', class_='header-right-menu__avatar')[0]['src'].split('/')[5]
        dump_info(id_)
        info[0]['id'] = id_ 

    mangas = []
    driver.get(mangalib + '/user/' + info[0]['id'])

    topics = ['r', 'p', 'd', 'e']

    for i, block in enumerate(driver.find_elements(By.CLASS_NAME, "menu__item")[1:6]):
        block.click()
        time.sleep(1)
        bs = bs4(driver.page_source, 'html.parser')
        for manga in bs.find_all('div', class_='bookmark-item__info'): 
            temp = manga.find_all('span')
            if 'Продолжить' not in temp[-1].text:
                chapter = '0'
            else:
                chapter = temp[-1].text.strip()
                chapter = chapter.split('-')[1][:-1]
            if i == 4:
                if float(manga.find('div', class_='bookmark-item__info-subheader').text.split()[-1]) <= float(chapter):
                    topic = 'e'
                topic = 'r'
            else:
                topic = topics[i]
            mangas.append(Manga(temp[0].text, topic, chapter))
    dump_info(info[0]['id'], mangas)

    driver.quit()

if __name__ == '__main__':
    mangalib_parse()