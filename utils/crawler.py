import time
import random
import concurrent.futures
from typing import List,Dict

import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

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

def all_pages(func):
    """ Function:- Loop through all pages """
    for page_num in range(1,10):
        time.sleep(random.uniform(1.0, 2.0))
        func(page_num)

with concurrent.futures.ThreadPoolExecutor() as executor:
    """Run concurrently using Threading module and collect link
    for every page 3 seconds time interval"""
    func = all_pages(get_all_Links)
    f1 = executor.submit(func, 3)

if __name__ == "__main__":
    link_data = f1
    df = pd.DataFrame(links)
    df.to_csv(r"./data/links.csv", index=False, header=True)