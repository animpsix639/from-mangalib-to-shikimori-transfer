from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs4
import time
import pickle
from mangalib_parser import mangalib_parse
import keyboard
from selenium.webdriver.common.keys import Keys

with open(r'C:\code\shiki  + mangalib\settings', 'rb') as f:
    info = pickle.load(f)
    if info[2] == '':
        mangalib_parse()

topics = {'r': 'Читаю',
          'p': 'Запланировано',
          'd': 'Брошено',
          'e': 'Прочитано',
          'f': 'Прочитано'}


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-ssl-errors')
options.add_argument(r'--disk-cache-dir=C:\code\shiki  + mangalib\cache')

driver = webdriver.Chrome(options=options)


driver.get("https://shikimori.me/users/sign_in")

driver.find_element(By.CLASS_NAME, 'b-link').click()
time.sleep(5)
driver.find_element(By.NAME, 'user[nickname]').send_keys(info[1]['login'])
driver.find_element(By.NAME, 'user[password]').send_keys(info[1]['password'])

print('!!!ВАЖНО!!! Введите капчу, а после выполнения нажмите клавишу \'C\'')
while True:
    if keyboard.is_pressed('c'):
        break
    else:
        continue

driver.find_element(By.NAME, 'commit').click()


for manga in info[2]:
    search = driver.find_element(By.XPATH, '//input[1]')
    search.click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[@data-mode='manga']").click()
    search.send_keys(manga.name)

    time.sleep(5)
    driver.find_element(By.XPATH, "//a[@class='b-db_entry-variant-list_item']").click()
    time.sleep(8)

    if driver.find_element(By.XPATH, "//span[@class='status-name']").text != 'Добавить в список':
        driver.find_element(By.XPATH, "//div[@class='trigger-arrow']").click()
        time.sleep(4)
        driver.find_element(By.XPATH, "//span[@data-text='Удалить из списка']").click()
        time.sleep(6)
    
    driver.find_element(By.XPATH, "//div[@class='trigger-arrow']").click()
    time.sleep(4)

    topic = topics[manga.topic]
    driver.find_element(By.XPATH, f"//span[@data-text='{topic}']").click()
    time.sleep(4)

    driver.find_element(By.XPATH, "//span[@class='status-name']").click()
    time.sleep(4)

    temp = driver.find_element(By.XPATH, "//input[@id='user_rate_chapters']")
    temp.send_keys(Keys.ARROW_RIGHT)
    temp.send_keys(Keys.BACKSPACE)
    temp.send_keys(manga.chapter)
    time.sleep(3)

    driver.find_element(By.XPATH, "//input[@name='commit']").click()
    time.sleep(4)

driver.quit()