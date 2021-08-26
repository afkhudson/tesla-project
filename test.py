from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
import time
import pandas as pd
import re

#https://www.carvana.com/cars/tesla
#https://shift.com/cars?search=tesla
#https://www.carvana.com/cars/tesla
#https://www.carmax.com/cars?search=tesla

#https://www.tesla.com/inventory/used/ms
#https://www.tesla.com/inventory/used/m3
#https://www.tesla.com/inventory/used/mx
#https://www.tesla.com/inventory/used/my


carvana1 = 'https://www.carvana.com/cars/tesla?filters=eyJtYWtlc2FuZG1vZGVscyI6W3sibWFrZVNsdWciOiJ0ZXNsYSJ9XSwicGFnZSI6OX0='
carvana2 = 'https://www.carvana.com/cars/tesla?filters=eyJtYWtlc2FuZG1vZGVscyI6W3sibWFrZVNsdWciOiJ0ZXNsYSJ9XSwicGFnZSI6OH0='
carvana = 'https://www.carvana.com/cars/tesla'
shift = 'https://shift.com/cars?search=tesla'
carvana = 'https://www.carvana.com/cars/tesla?email-capture=&page=2'
carmax = 'https://www.carmax.com/cars?search=tesla'

tesla_ms = 'https://www.tesla.com/inventory/used/ms'
tesla_m3 = 'https://www.tesla.com/inventory/used/m3'
tesla_mx = 'https://www.tesla.com/inventory/used/mx'
tesla_my = 'https://www.tesla.com/inventory/used/my'

options = Options()
options.headless = False
options.add_argument("--enable-javascript")

browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)


#starting browser
def carvana_scrape():

    data = {'url': [],
	'model': [],
	'year': [],
    'price': [],
    'miles': [],
    'type': [],
    'color': [],
	'status': [],
    'image': []}


    carvana_df = pd.DataFrame(data)
    print(carvana_df)
    browser.get(carvana)
    browser.set_page_load_timeout(20)
    next_button = True
    last_url = ''
    while next_button:
        try:
            browser.find_element_by_xpath('/html/body/div[2]/main/div[2]/div/button/div[2]/svg/path').click()
            browser.find_element_by_xpath('/html/body/div[2]/main/div[2]/div/div[3]/svg'.close())
        except:
            pass
        print(last_url)
        print(browser.current_url)
        if last_url == browser.current_url:
            next_button = False
            break
        elements = browser.find_elements_by_css_selector('article.result-tile')
        time.sleep(1)
        print(elements)
        print(f'found: {len(elements)}')
        #go through each element of first page
        for element in elements:
            model_check = element.find_elements_by_class_name('model')
            url_check = element.find_elements_by_xpath(f'/html/body/div[2]/main/section/section/article[{elements.index(element)+1}]/a')
            if not url_check or not model_check:
                continue
            else:
                time.sleep(1)
                statuslol = browser.find_elements_by_xpath(f'//*[@id="results-section"]/article[{elements.index(element)+1}]/a/div[2]/span')
                print(statuslol[0].get_attribute('innerHTML'))
                #find details of each element
                #image = element.find_element_by_class_name(f'/html/body/div[1]/div/div/div[2]/div[2]/div[5]/a[{elements.index(element)+1}]/div/div/div[1]/img').get_attribute('src')
                image = WebDriverWait(browser, 1).until(EC.visibility_of_element_located((By.CLASS_NAME, "image-wrapper"))).get_attribute("src")
                #image = element.find_element_by_css_selector('img._3WEbGjQbERZrIJuNiXxofi').get_attribute('src')
                #url = WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.XPATH, f"/html/body/div[2]/main/section/section/article[{elements.index(element)+1}]/a"))).get_attribute('href')
                url = element.find_element_by_xpath(f'/html/body/div[2]/main/section/section/article[{elements.index(element)+1}]/a').get_attribute('href')
                model = element.find_element_by_class_name(f'model').get_attribute('innerHTML')[-7:]
                year = int(element.find_element_by_class_name(f'year-make').get_attribute('innerHTML')[:4])
                price = element.find_element_by_class_name(f'price').get_attribute('innerHTML')[12:]
                num_price = re.sub("[^0-9]", "", price)
                miles = element.find_element_by_class_name(f'mileage').get_attribute('innerHTML')[:-14]
                num_miles = re.sub("[^0-9]", "", miles)
                type = element.find_element_by_class_name(f'trim').get_attribute('innerHTML')
                color = 'color'
                status_check = element.find_elements_by_xpath(f'//*[@id="results-section"]/article[{elements.index(element)+1}]/a/div[2]/span')
                print(status_check)
                if not status_check:
                    status = "Available Now"
                else:
                    status = status_check[0].get_attribute('innerHTML')
                print(url, model, year, price, miles, type, color, status, image)
                new_row = {'url': url, 'model': model, 'year': int(year), 'price': int(num_price), 'miles': num_miles, 'type': type, 'color': color, 'status': status, 'image': image}
                carvana_df = carvana_df.append(new_row, ignore_index=True)
        #browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        #next_button_clickable = browser.find_elements_by_xpath('/html/body/div[1]/div/div/div[2]/div[2]/div[6]/div[4]/div/button/div[2]')
        #browser.execute_script("return arguments[0].scrollIntoView();", browser.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[2]/div[6]'))
        #browser.execute_script("window.scrollTo(0,document.body.scrollHeight*0.5);")

        next_button_clickable = WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/main/section/ul/li[3]/button[1]")))

        #print(len(next_button_clickable))
        last_url = browser.current_url
        time.sleep(1)
        #next_button_clickable.click()
        time.sleep(1)
        #time.sleep(0.5)

carvana_scrape()
