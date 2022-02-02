import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from typing import List
import lxml
from csv import reader
import concurrent.futures


class Cleaner:
    # a list of everything that the exercice ask
    list_asked: List[str] = [
        "Price",
        "Bathrooms",
        "Living area",
        "Kitchen type",
        "Furnished",
        "How many fireplaces?",
        "Terrace surface",
        "Garden Surface",
        "Surface of the plot",
        "Number of frontages",
        "Swimming pool",
        "Building condition",
        "Subtype of property",
        "Locality",
        "Postal_code",
    ]
    list_yes_or_no: List[str] =[
        "Living area",
        "Furnished",
        "Terrace surface",
        "Garden Surface",
        "Surface of the plot",
        "Swimming pool",
        "Kitchen type"
    ]

    def __init__(self):
        self.output = {k: [] for k in list(self.list_asked)}

    def getData(self, url) -> dict:
        """
        to get all the data we need that we can found in the web table
        """

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml").prettify()
        price = BeautifulSoup(response.text, "lxml").select('div.classified__header-primary-info p.classified__price span.sr-only')[0].string


        regex: str = "[^\/]+"
        dividedUrl: List[str] = re.findall(regex, url)

        subtypeOfProperty: str = dividedUrl[4]
        self.output["Subtype of property"].append(subtypeOfProperty)
        self.output["Locality"].append(dividedUrl[6])
        self.output["Postal_code"].append(dividedUrl[7])
        self.output["Price"].append(price)

        tables: DataFrame = pd.read_html(soup)


        num_table = len(tables)
        all_tables = [tables[idx] for idx in range(num_table)]

        # fmt:off
        df = pd.concat(all_tables)

        for _, v in df.iterrows():
            if v[0] in self.list_asked:
                key = v[0]
                value = v[1]

                # Clean up
                if key == "Price":
                    value = value.split(" ")[3]
                elif key in self.list_yes_or_no and value == "No":
                    value = 0
                elif key in ["Living area", "Terrace surface", "Garden Surface", "Surface of the plot"]:
                    value = value.split(" ")[0]

                if key == "Kitchen type":
                    value = 1
                    if key == "Not installed":
                        value = 0

                for item in self.list_asked:
                    if key == item:
                        self.output[key].append(value)

        # fill empty column
        for k in self.list_yes_or_no:
            if not self.output[k]:
                self.output[k].append(0)

        for k in self.list_asked:
            if not self.output[k]:
                self.output[k].append(None)

        return self.output


if __name__ == "__main__":

    # url = "https://www.immoweb.be/en/classified/town-house/for-sale/laeken/1020/9730456?searchId=61f79f25891ae"

    dealer = Cleaner()

    df = pd.read_csv(r'./data/property_link.csv')
    links = df.link.to_list()
    url = links[0]

    result = dealer.getData(url)
    print(result)

    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     """Run concurrently using Threading module and collect link
    #     for every the pages mentioned in the list"""
    #     f1 = executor.map(dealer.getData, links)

    # for f in f1:
    #     print(f)
