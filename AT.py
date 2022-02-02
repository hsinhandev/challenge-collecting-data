# import bs4
# import requests
# from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
# import re
# import lxml.html
# import time
from random import randint
# import concurrent.futures

# import re
# import os
from typing import List, Dict

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

service = Service("C:\\chromedriver_win32\\chromedriver.exe")
driver = webdriver.Chrome(service = service, options = options)   # to fix 

def extract_property_link(num_pages: int) -> List[str]:

    """[Extrat property link from websites]
    Args:
        num_pages (int): [pages index]
    Returns:
        [type]: [List[str]]
    """

    print(f"====== Collection pages {num_pages}")

    immoweb_url_pages = f"https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&page={num_pages}&orderBy=relevance"
    driver.get(immoweb_url_pages)

    
    property_list = driver.find_elements(By.CSS_SELECTOR, "ul#main-content article a")
    property_link = []
    for link in property_list:
        property_link.append(link.get_attribute("href"))
    
    

    print(f"====== Collection pages {num_pages} Finished =======")
    return property_link

def get_property_link_until_ten_thousnad() -> Dict[str, str]:
    """[This function should call extract_property_link until 10,000 property link]
    Returns:
        [type]: [description]
    """
    properties_link = {"link": []}

    # TODO fix crash at page 12
    for num in range(1, 300):
        for href in extract_property_link(num):
            properties_link["link"].append(href)
    return properties_link

# with concurrent.futures.ThreadPoolExecutor() as executor:
#     """Run concurrently using Threading module and collect link
#     for every page 3 seconds time interval"""
#     func = get_property_link_until_ten_thousnad()
#     f1 = executor.submit(func, 3)

if __name__ == "__main__":
  property_link_output = get_property_link_until_ten_thousnad()
  df = pd.DataFrame(property_link_output)
  df.to_csv(r"./challenge-collecting-data/Data/property_link.csv", index=False, header=True)

driver.quit()


