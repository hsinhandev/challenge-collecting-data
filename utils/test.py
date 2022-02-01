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

@property
def getGardenSurface(self):
    url = "https://www.immoweb.be/en/classified/town-house/for-sale/laeken/1020/9730456?searchId=61f79f25891ae"

    response = requests.get(url)

    regex = "[0-9]+"

    soup = BeautifulSoup(response.content, "lxml")

    plot = soup.select("tr.classified-table__row")

    for i,elem in enumerate(plot):

        for x,subElem in enumerate(elem):
            if str(subElem).find("Garden surface") != -1:

                myArray = elem.select_one("td")
                
                gardenSurface:int = re.findall(regex,str(myArray))[0]
            
    return int(gardenSurface)
                

