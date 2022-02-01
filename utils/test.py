from asyncio.base_subprocess import BaseSubprocessTransport
from threading import local
import requests
from bs4 import BeautifulSoup
import lxml
import re
from selenium.webdriver.firefox.webdriver import WebDriver
import selenium
from selenium.webdriver.common.by import By
import time
from typing import List


def getAddresse(self) -> List[str]:
    
    url = "https://www.immoweb.be/en/classified/town-house/for-sale/laeken/1020/9730456?searchId=61f79f25891ae"

    driver = WebDriver()

    driver.get(url)

    driver.minimize_window()

    driver.implicitly_wait(10)

    address:List[str] = driver.find_elements(By.CLASS_NAME,"classified__information--address-row")

    #subdivised in cas we need the information in a more specific way (adress = street + code + localityName)

    street:str = address[0].text

    locality = address[1].text

    locality:str = locality.strip()

    code,dash,localityName = locality.split()

    fullLocality:List[str] = []

    fullLocality.append(street)
    fullLocality.append(code)
    fullLocality.append(dash)
    fullLocality.append(localityName)

    driver.close()

    return fullLocality


