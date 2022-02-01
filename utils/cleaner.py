import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

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