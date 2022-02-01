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

    def extract_property_info():
        """[Extract infomation from each property]"""

        property_csv_path = os.path.join(
            os.path.dirname(__file__), "../data/property_link.csv"
        )

        df = pd.read_csv(property_csv_path)
        output = {}
        for link in df["link"]:
            html = requests.get(link)
            soup = BeautifulSoup(html.content, "lxml")

            list_container = soup.find_all("dl", attrs={"class": "wpis-detail-list"})
            for idx, tag in enumerate(list_container):

                # skip rapport Energetique
                if idx == 3:
                    continue

                print(tag.get_text(" | "))
            break


    if __name__ == "__main__":
        extract_property_info()

    target_attributes = (
        "Locality",
        "Type of property",
        "Subtype of property",
        "Price",
        "Type of sale",
        "Number of rooms",
        "Area",
        "State of the building " "Surface of the land",
        "Surface area of the plot of land",
        "Number of facades",
        "Swimming pool",
        "Fully equipped kitchen",
        "Furnished",
        "Open fire ",
        "Terrace",
        "Garden",
    )

    target_attributes_FR = (
        "Locality",
        "Type du bien",
        "Subtype of property",
        "Prix",
        "Disponibilité",
        "Number of rooms",
        "Ville",
        "État du bien",
        "Surface of the land",
        "Surface area of the plot of land",
        "Number of facades",
        "Swimming pool",
        "Fully equipped kitchen",
        "Furnished",
        "Open fire ",
        "Terrace",
        "Garden",
    )

    @property
    def getSurface(self):

        url = "https://www.immoweb.be/en/classified/town-house/for-sale/laeken/1020/9730456?searchId=61f79f25891ae"

        response = requests.get(url)

        soup = BeautifulSoup(response.content, "lxml")

        livingArea = soup.select("td.classified-table__data")

        for i,elem in enumerate(livingArea):
            if i == 10:
                regex = "[0-9]+"
                surface = re.findall(regex,str(elem))[0]

        return int(surface)


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
def getSurfacePlot(self):
    """
    to get the surface of the plot for one property
    """
    url = "https://www.immoweb.be/en/classified/town-house/for-sale/laeken/1020/9730456?searchId=61f79f25891ae"

    response = requests.get(url)

    regex = "[0-9]+"

    soup = BeautifulSoup(response.content, "lxml")

    plot = soup.select("tr.classified-table__row")

    for i,elem in enumerate(plot):

        for x,subElem in enumerate(elem):
            if str(subElem).find("Surface of the plot") != -1:
                myArray = elem.select_one("td")
                
    surfacePlot = re.findall(regex,str(myArray))[0]


    return int(surfacePlot)


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


@property
def getTerraceSurface(self):
    url = "https://www.immoweb.be/en/classified/town-house/for-sale/laeken/1020/9730456?searchId=61f79f25891ae"

    response = requests.get(url)

    regex = "[0-9]+"

    soup = BeautifulSoup(response.content, "lxml")

    plot = soup.select("tr.classified-table__row")

    for i,elem in enumerate(plot):

        for x,subElem in enumerate(elem):
            if str(subElem).find("Terrace surface") != -1:

                myArray = elem.select_one("td")
                
                terraceSurface:int = re.findall(regex,str(myArray))[0]
            
    return int(terraceSurface)