import time
import random
import concurrent.futures
from tracemalloc import start
from typing import List,Dict

import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

started = time.perf_counter()
links = []
def get_all_Links(page_num):
    """Function:- Find all links for house and apartment"""

    url = f"https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&page={page_num}&orderBy=relevance"

    #options = webdriver.ChromeOptions()
    #options.add_argument('headless')
    driver = webdriver.Chrome()
    # Here, we create instance of Chrome WebDriver.
    driver.get(url)

    elem = driver.find_elements(By.CSS_SELECTOR, 'ul#main-content article a')
    print(elem)
    for link in elem:
       links.append(link.get_attribute('href'))

    driver.quit()

    return links    

with concurrent.futures.ThreadPoolExecutor() as executor:
    """Run concurrently using Threading module and collect link
    for every the pages mentioned in the list"""
    #func = all_pages(get_all_Links)
    page = [1,2,3,4,5,6,7,8,9,10]
    f1 = executor.map(get_all_Links, page)

if __name__ == "__main__":
    df = pd.DataFrame(links)
    df.to_csv(r"./data/links.csv", index=False, header=True)
