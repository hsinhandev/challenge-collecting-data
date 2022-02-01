import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import selenium
from selenium.webdriver.firefox.webdriver import WebDriver
from typing import List
from selenium.webdriver.common.by import By
from pandas import DataFrame
from pandas import read_html

class Cleaner:

    def __init__(self):
        pass


    @property
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

    @property
    def getData(self) -> dict:
        """
        to get all the data we need that we can found in the web table
        """

        url = "https://www.immoweb.be/en/classified/town-house/for-sale/laeken/1020/9730456?searchId=61f79f25891ae"

        response = requests.get(url)

        myData:dict = {}

        regex:str = "[^\/]+"

        dividedUrl:List[str] = re.findall(regex,url)

        subtypeOfProperty:str = dividedUrl[4]

        locality:str = dividedUrl[6] + " " + dividedUrl[7]

        myData["Subtype of property"] = subtypeOfProperty

        myData["Locality"] = locality

        soup = BeautifulSoup(response.content, "lxml")

        soup2 = soup.prettify()

        tables:DataFrame  = read_html(soup2)

        general:DataFrame = tables[0]

        interior:DataFrame  = tables[1]

        exterior:DataFrame  = tables[2]

        facilities:DataFrame  = tables[3]

        energy:DataFrame  = tables[4]

        townPlanning:DataFrame  = tables[5]

        financial:DataFrame  = tables[6]


        #put the sub data frame in a list to a easy acces in the loop
        titles:List[DataFrame] = [
            general,
            interior,
            exterior,
            facilities,
            energy,
            townPlanning,
            financial
        ]


        #a list of everything that the exercice ask
        listAsked:List[str] = [
            "Price",
            "Bathrooms",
            "Living area",
            "Kitchen type",
            "Furnished",
            "How many fireplaces?",
            "Terrace surface","Garden Surface",
            "Surface of the plot",
            "Number of frontages",
            "Swimming pool",
            "Building condition"
        ]

    
        for title in titles:

            for firstColumn,secondColumn in title.iterrows():

                key = secondColumn[0]
                value = secondColumn[1]

                for item in listAsked:

                    if key == item:

                        myData[key] = value


        return myData
