from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import re
from datetime import date
from datetime import datetime
import threading


today = date.today()
d4 = today.strftime("%Y%m%d")
print(d4)

#datetime object for excel
datetime_object = datetime.strptime(d4, '%Y%m%d')
print(datetime_object)

#https://www.vroom.com/cars/tesla
#https://shift.com/cars?search=tesla
#https://www.carvana.com/cars/tesla
#https://www.carmax.com/cars?search=tesla

#https://www.tesla.com/inventory/used/ms
#https://www.tesla.com/inventory/used/m3
#https://www.tesla.com/inventory/used/mx
#https://www.tesla.com/inventory/used/my

vroom = 'https://www.vroom.com/cars/tesla'
shift = 'https://shift.com/cars?search=tesla'
carvana = 'https://www.carvana.com/cars/tesla'
carmax = 'https://www.carmax.com/cars?search=tesla'

tesla_ms = 'https://www.tesla.com/inventory/used/ms'
tesla_m3 = 'https://www.tesla.com/inventory/used/m3'
tesla_mx = 'https://www.tesla.com/inventory/used/mx'
tesla_my = 'https://www.tesla.com/inventory/used/my'

options = Options()
options.headless = False



#starting browser
def vroom_scrape():
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    data = {'url': [],
	'model': [],
	'year': [],
    'price': [],
    'miles': [],
    'type': [],
    'color': [],
	'status': [],
    'image': []}

    vroom_df = pd.DataFrame(data)
    print(vroom_df)
    browser.get(vroom)
    browser.set_page_load_timeout(10)
    next_button = True
    last_url = ''
    count = 0
    while next_button:
        print(last_url)
        print(browser.current_url)
        if last_url == browser.current_url:
            next_button = False
        elements = browser.find_elements_by_xpath("//div[@data-element='Grid']")
        print(elements)
        print(f'found: {len(elements)}')
        #go through each element of first page
        for element in elements:
            #find details of each element
            #url = element.find_element_by_xpath(f'//*[@id="__next"]/div/div/div[3]/div/div[2]/div/div[{elements.index(element)+1}]/div/a').get_attribute('href')
            url = element.find_elements_by_xpath("//a[@data-element='HiddenAnchor']")[count].get_attribute('href')
            count += 1
            #img
            image = element.find_elements_by_xpath("//img[@data-element='Photo']")[elements.index(element)].get_attribute('src')
            model = element.find_element_by_xpath(f'/html/body/div[1]/div/div/div[3]/div/div[2]/div/div[{elements.index(element)+1}]/div/a/div[2]/div/p[1]').get_attribute('innerHTML')[-7:]
            year = int(element.find_element_by_xpath(f'//*[@id="__next"]/div/div/div[3]/div/div[2]/div/div[{elements.index(element)+1}]/div/a/div[2]/div/p[1]').get_attribute('innerHTML')[:4])
            price = element.find_element_by_xpath(f'/html/body/div[1]/div/div/div[3]/div/div[2]/div/div[{elements.index(element)+1}]/div/a/div[2]/div/p[2]').get_attribute('innerHTML')
            num_price = re.sub("[^0-9]", "", price)
            miles = element.find_element_by_xpath(f'/html/body/div[1]/div/div/div[3]/div/div[2]/div/div[{elements.index(element)+1}]/div/a/div[2]/div/div/p[2]').get_attribute('innerHTML')[:-6]
            num_miles = re.sub("[^0-9]", "", miles)
            type = element.find_element_by_xpath(f'/html/body/div[1]/div/div/div[3]/div/div[2]/div/div[{elements.index(element)+1}]/div/a/div[2]/div/div/p[1]').get_attribute('innerHTML')
            color = 'color'
            status_check = element.find_elements_by_xpath(f'/html/body/div[1]/div/div/div[3]/div/div[2]/div/div[{elements.index(element)+1}]/div/a/div[2]/p')
            if len(status_check) == 0:
                status = "Available Now"
            else:
                status = element.find_elements_by_xpath(f'/html/body/div[1]/div/div/div[3]/div/div[2]/div/div[{elements.index(element)+1}]/div/a/div[2]/p')[0].get_attribute('innerHTML')
            print(url, model, year, price, miles, type, color, status, image)
            new_row = {'url': url, 'model': model, 'year': int(year), 'price': int(num_price), 'miles': int(num_miles), 'type': type, 'color': color, 'status': status, 'image': image}
            vroom_df = vroom_df.append(new_row, ignore_index=True)
        next_button_clickable = browser.find_elements_by_xpath('/html/body/div[1]/div/div/div[3]/div/nav/ul/li[9]')
        print(len(next_button_clickable))
        last_url = browser.current_url
        next_button_clickable[0].click()
        count = 0
        time.sleep(.5)
        #time.sleep(0.5)
    writer = pd.ExcelWriter(f'vroom/{d4} vroom-test.xlsx')
    vroom_df.to_excel(writer, index=False)
    writer.save()
    print(vroom_df)
    print('no more pages')

def shift_scrape():
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    data = {'url': [],
	'model': [],
	'year': [],
    'price': [],
    'miles': [],
    'type': [],
    'color': [],
	'status': [],
    'image': []}


    shift_df = pd.DataFrame(data)
    print(shift_df)
    browser.get(shift)
    browser.set_page_load_timeout(20)
    next_button = True
    last_url = ''
    while next_button:
        print(last_url)
        print(browser.current_url)
        if last_url == browser.current_url:
            next_button = False
            break
        elements = browser.find_elements_by_css_selector('div.ipvdwWzbIGcTmfsYJ30bu')
        time.sleep(1)
        print(elements)
        print(f'found: {len(elements)}')
        #go through each element of first page
        for element in elements:
            #find details of each element
            #image = element.find_element_by_xpath(f'/html/body/div[1]/div/div/div[2]/div[2]/div[5]/a[{elements.index(element)+1}]/div/div/div[1]/img').get_attribute('src')
            image = element.find_element_by_tag_name('img').get_attribute('data-src')
            #image = element.find_element_by_css_selector('img._3WEbGjQbERZrIJuNiXxofi').get_attribute('src')
            url = element.find_element_by_xpath(f'/html/body/div[1]/div/div/div[2]/div[2]/div[5]/a[{elements.index(element)+1}]').get_attribute('href')
            model = element.find_element_by_xpath(f'/html/body/div[1]/div/div/div[2]/div[2]/div[5]/a[{elements.index(element)+1}]/div/div/div[2]/div[1]/div[1]/div[2]').get_attribute('innerHTML')[-7:]
            year = int(element.find_element_by_xpath(f'/html/body/div[1]/div/div/div[2]/div[2]/div[5]/a[{elements.index(element)+1}]/div/div/div[2]/div[1]/div[1]/div[1] ').get_attribute('innerHTML')[:4])
            price = element.find_element_by_xpath(f'/html/body/div[1]/div/div/div[2]/div[2]/div[5]/a[{elements.index(element)+1}]/div/div/div[2]/div[1]/div[2]/div[1]').get_attribute('innerHTML')
            num_price = re.sub("[^0-9]", "", price)
            miles = element.find_element_by_xpath(f'/html/body/div[1]/div/div/div[2]/div[2]/div[5]/a[{elements.index(element)+1}]/div/div/div[2]/div[1]/div[1]/div[3]/div[2]').get_attribute('innerHTML')[:-7]
            num_miles = int(miles)*1000
            type = element.find_element_by_xpath(f'/html/body/div[1]/div/div/div[2]/div[2]/div[5]/a[{elements.index(element)+1}]/div/div/div[2]/div[1]/div[1]/div[3]/div[1]').get_attribute('innerHTML')
            color = 'color'
            status_check = element.find_elements_by_xpath(f'/html/body/div[1]/div/div/div[2]/div[2]/div[5]/a[{elements.index(element)+1}]/div/div/div[1]/div[2]/span')
            if not status_check:
                status = "Available Now"
            else:
                status = element.find_elements_by_xpath(f'/html/body/div[1]/div/div/div[2]/div[2]/div[5]/a[{elements.index(element)+1}]/div/div/div[1]/div[2]/span')[0].get_attribute('innerHTML')
            print(url, model, year, price, miles, type, color, status, image)
            new_row = {'url': url, 'model': model, 'year': int(year), 'price': int(num_price), 'miles': num_miles, 'type': type, 'color': color, 'status': status, 'image': image}
            shift_df = shift_df.append(new_row, ignore_index=True)
        #browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        try:
            browser.find_element_by_class_name('ub-emb-close').click()
        except:
            print('close button error')
        #next_button_clickable = browser.find_elements_by_xpath('/html/body/div[1]/div/div/div[2]/div[2]/div[6]/div[4]/div/button/div[2]')
        #browser.execute_script("return arguments[0].scrollIntoView();", browser.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[2]/div[6]'))
        #browser.execute_script("window.scrollTo(0,document.body.scrollHeight*0.5);")

        next_button_clickable = WebDriverWait(browser, 20).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/div[2]/div[6]/div[4]/div/button/div[2]")))

        #print(len(next_button_clickable))
        last_url = browser.current_url
        time.sleep(1)
        try:
            next_button_clickable.click()
        except:
            print('cant click next button')
        time.sleep(1)
        #time.sleep(0.5)
    writer = pd.ExcelWriter(f'shift/{d4} shift-test.xlsx')
    shift_df.to_excel(writer, index=False)
    writer.save()
    print(shift_df)
    print('no more pages')

def carvana_scrape():
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)

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
    browser.set_page_load_timeout(50)
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
        elements = browser.find_elements_by_xpath("//div[@data-test='ResultTile']")
        print(elements)
        print(f'found: {len(elements)}')
        #go through each element of first page
        for element in elements:
            #check available
            status_check = element.find_elements_by_class_name(f'purchase-callout')
            if len(status_check) == 0:
                status = "Available"
            else:
                status_text = status_check[0].get_attribute('class').split(" ")[1].title()
                status = status_text

            image_check = element.find_elements_by_xpath(f'//*[@id="results-section"]/article[{elements.index(element)+1}]/a/div[1]/img')
            if len(image_check) > 0:
                image = element.find_elements_by_xpath("//img[@loading='lazy']")[elements.index(element)].get_attribute('src')
            else:
                image = element.find_elements_by_xpath("//img[@loading='lazy']")[elements.index(element)].get_attribute('src')

            url = element.find_elements_by_xpath("//a[contains(@href, '/vehicle/')]")[elements.index(element)].get_attribute('href')

            model = element.find_element_by_class_name(f'model').get_attribute('innerHTML')[-7:]
            year = int(element.find_element_by_class_name(f'year-make').get_attribute('innerHTML')[:4])

            price = element.find_element_by_class_name(f'price').get_attribute('innerHTML')[12:]
            num_price = ''.join(filter(lambda x: x.isdigit(), price))

            miles = element.find_element_by_class_name('mileage').get_attribute('innerHTML')
            num_miles = ''.join(filter(lambda x: x.isdigit(), miles))

            type = element.find_element_by_class_name(f'trim').get_attribute('innerHTML')
            color = 'color'
            print(url, model, year, num_price, num_miles, type, color, status, image)
            new_row = {'url': url, 'model': model, 'year': int(year), 'price': int(num_price), 'miles': int(num_miles), 'type': type, 'color': color, 'status': status, 'image': image}
            carvana_df = carvana_df.append(new_row, ignore_index=True)

        try:
            next_button_clickable = WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/main/section/ul/li[3]/button[1]")))
            time.sleep(1)
            next_button_clickable.click()
        except:
            print('---CANT CLICK NEXT')

        #print(len(next_button_clickable))
        last_url = browser.current_url
        time.sleep(1)
        #time.sleep(0.5)
    writer = pd.ExcelWriter(f'carvana/{d4} carvana-test.xlsx')
    carvana_df.to_excel(writer, index=False)
    writer.save()
    print(carvana_df)
    print('no more pages')


def tesla_scrape(site, name):
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    data = {'url': [],
	'model': [],
	'year': [],
    'price': [],
    'miles': [],
    'type': [],
    'color': [],
	'status': [],
    'image': []}


    tesla_df = pd.DataFrame(data)
    print(tesla_df)
    browser.get(site)
    time.sleep(2)
    browser.set_page_load_timeout(20)
    next_button = True
    last_url = ''

    def scroll_down():
        """A method for scrolling the page."""

        # Get scroll height.
        last_height = browser.execute_script("return document.body.scrollHeight")

        while True:

            # Scroll down to the bottom.
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load the page.
            time.sleep(2)

            # Calculate new scroll height and compare with last scroll height.
            new_height = browser.execute_script("return document.body.scrollHeight")

            if new_height == last_height:

                break

            last_height = new_height
    main_title = browser.title
    print(main_title)
    scroll_down()
    time.sleep(2)
    browser.execute_script("window.scrollTo(0, 220)")
    elements = browser.find_elements_by_class_name('result.card')
    time.sleep(1)
    print(elements)
    print(f'found: {len(elements)}')
    #go through each element of first page
    count = 1
    for element in elements:
        # try:
        scroll_to = element.find_element_by_class_name('result-gallery')
        #model_check = element.find_elements_by_class_name('model')
        #url_check = element.find_elements_by_xpath(f'/html/body/div[2]/main/section/section/article[{elements.index(element)+1}]/a')
        #check available
        image = element.find_element_by_xpath(f'//*[@id="iso-container"]/div/div[1]/main/div/article[{elements.index(element)+1}]/section[2]/div/ul/li[1]/div/div[2]/img').get_attribute('src')
        buy_button = element.find_element_by_class_name(f'result-buy-btn')
        hover = element.find_element_by_class_name('result-features')
        browser.execute_script("arguments[0].scrollIntoView();", scroll_to)
        time.sleep(0.5)
        action = ActionChains(browser)
        action.move_to_element(hover)
        action.perform()
        buy_button.click()

        main_window = browser.current_window_handle
        browser.switch_to_window(main_window)
        browser.switch_to.window(browser.window_handles[count])
        url = browser.current_url[:48]

        if url == 'https://www.tesla.com/ms/order/inventory/used/ms#payment':
            continue

        color = browser.find_element_by_xpath(f'/html/body/div[1]/div[2]/main/section/div[2]/div/div[2]/div/div/div[2]/ol/li[2]/p/span').get_attribute('innerHTML') #gets color from new page
        count += 1
        browser.switch_to.window(browser.window_handles[0])

        model = element.find_element_by_xpath(f'//*[@id="iso-container"]/div/div[1]/main/div/article[{elements.index(element)+1}]/section[1]/div[1]/h3/span[2]').get_attribute('innerHTML')
        year = int(element.find_element_by_xpath(f'//*[@id="iso-container"]/div/div[1]/main/div/article[{elements.index(element)+1}]/section[1]/div[1]/h3/span[1]').get_attribute('innerHTML'))

        price = element.find_element_by_xpath(f'//*[@id="iso-container"]/div/div[1]/main/div/article[{elements.index(element)+1}]/section[1]/div[2]/div[1]/span').get_attribute('innerHTML')
        num_price = ''.join(filter(lambda x: x.isdigit(), price))

        miles = element.find_element_by_xpath(f'//*[@id="iso-container"]/div/div[1]/main/div/article[{elements.index(element)+1}]/section[1]/div[1]/div[2]').get_attribute('innerHTML')[:-14]
        num_miles = ''.join(filter(lambda x: x.isdigit(), miles))
        type = element.find_element_by_class_name(f'tds-text_color--10').get_attribute('innerHTML')
        print(url, model, year, num_price, num_miles, type, color, 'Available Now', image)
        new_row = {'url': url, 'model': model, 'year': int(year), 'price': int(num_price), 'miles': int(num_miles), 'type': type, 'color': color, 'status': 'Available Now', 'image': image}
        tesla_df = tesla_df.append(new_row, ignore_index=True)
        # except:
        #     print('error in element')
        #     new_row = {'url': 'error', 'model': 'error', 'year': 'error', 'price': 'error', 'miles': 'error', 'type': 'error', 'color': 'error', 'status': 'error', 'image': 'error'}
        #     tesla_ms_df = tesla_ms_df.append(new_row, ignore_index=True)
    writer = pd.ExcelWriter(f'C:/Users/sosa/OneDrive/Coding/tesla-project/{name}/{d4} {name}-test.xlsx')
    tesla_df.to_excel(writer, index=False)
    writer.save()
    print(tesla_df)
    print('no more pages')


t1 = threading.Thread(target = shift_scrape)
t2 = threading.Thread(target = vroom_scrape)
t3 = threading.Thread(target = carvana_scrape)
t4 = threading.Thread(target = tesla_scrape, args = (tesla_ms,'tesla_ms',))
t6 = threading.Thread(target = tesla_scrape, args = (tesla_m3,'tesla_m3',))
t5 = threading.Thread(target = tesla_scrape, args = (tesla_mx,'tesla_mx',))
t7 = threading.Thread(target = tesla_scrape, args = (tesla_my,'tesla_my',))

def runall():
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    time.sleep(5)
    t5.start()
    time.sleep(5)
    t6.start()
    time.sleep(5)
    t7.start()
    time.sleep(5)

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    t7.join()

runall()
# tesla_ms_scrape()
# tesla_m3_scrape()
# vroom_scrape()
# tesla_scrape(tesla_ms,'tesla_ms')
