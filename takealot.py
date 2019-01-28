import bs4 as bs
import urllib.request
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time
import re
from selenium.common.exceptions import NoSuchElementException
import mongo_conf
from mongo_conf import GraphicsCards, compare_collections, increase_var_value


browser_options = Options()
browser_options.headless = True

driver = webdriver.Firefox(options=browser_options, executable_path="C:/Users/Riyaaz/Downloads/geckodriver-v0.23.0-win64/geckodriver.exe")


def get_gpu_details():
        driver.get("https://www.takealot.com/computers/graphics-cards-10100?sort=Price%20Ascending&rows=50&start=0&filter=Available:true&filter=Shipping:0")
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        item_name = soup.find_all('p', {'class' : 'p-title fn'})    
        item_price = soup.find_all('span', {'class' : 'amount'})
        scraped_items = zip(item_name, item_price)
        for item, price in scraped_items:
                cleaned_item_price = re.sub('[^A-Za-z0-9]+', '', price.text)
                cleaned_item_name = item.text
                data_set = GraphicsCards(item_name = cleaned_item_name, item_price = cleaned_item_price)
                data_set.save()

        if check_exists("page-plus-one") == True:       
                driver.find_element_by_class_name("page-plus-one").click()
                print("Clicking next button")
                time.sleep(3)
                get_gpu_details()
        else:
                print("Done")
                driver.quit()

def check_exists(classname):
    try:
        driver.find_element_by_class_name(classname)
    except NoSuchElementException:
        return False
    return True

if __name__ == "__main__":
    get_gpu_details()
    increase_var_value()
    compare_collections()

