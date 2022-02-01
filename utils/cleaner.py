import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import selenium
from selenium.webdriver.firefox.webdriver import WebDriver
from typing import List
from selenium.webdriver.common.by import By

class Cleaner:

    def __init__(self):
        pass
    

    #@property
    def getAddresse(self) -> List[str]:
        """
        subdivised in cas" we need the information in a more specific way 
        (adress = street + code + localityName)
        """
    
        url = "https://www.immoweb.be/en/classified/town-house/for-sale/laeken/1020/9730456?searchId=61f79f25891ae"

        driver = WebDriver()

        driver.get(url)

        driver.minimize_window()

        driver.implicitly_wait(10)

        address:List[str] = driver.find_elements(By.CLASS_NAME,"classified__information--address-row")

        #address = street + locality
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


    #@property
    def getNumbers(self,itemWeWant:str) -> int:

        url = "https://www.immoweb.be/en/classified/town-house/for-sale/laeken/1020/9730456?searchId=61f79f25891ae"

        response = requests.get(url)

        regex = "[0-9]+"

        soup = BeautifulSoup(response.content, "lxml")

        plot = soup.select("tr.classified-table__row")

        for i,elem in enumerate(plot):

            for x,subElem in enumerate(elem):
                if str(subElem).find(itemWeWant) != -1:

                    myArray = elem.select_one("td")
                    
                    numbers:int = re.findall(regex,str(myArray))[0]
                
        return int(numbers)


