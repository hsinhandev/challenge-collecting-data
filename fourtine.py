import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from typing import List
import lxml


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

    def __init__(self):
        self.output = {k: [] for k in list(self.list_asked)}

    def getData(self, url) -> dict:
        """
        to get all the data we need that we can found in the web table
        """

        response = requests.get(url)
        # myData: dict = {}
        regex: str = "[^\/]+"
        dividedUrl: List[str] = re.findall(regex, url)
        subtypeOfProperty: str = dividedUrl[4]
        # locality: str = dividedUrl[6] + " " + dividedUrl[7]
        self.output["Subtype of property"].append(subtypeOfProperty)
        self.output["Locality"].append(dividedUrl[6])
        self.output["Postal_code"].append(dividedUrl[7])

        # soup = BeautifulSoup(response.content, "lxml")
        # soup2 = soup.prettify()
        soup = BeautifulSoup(response.text, "lxml").prettify()
        tables: DataFrame = pd.read_html(soup)

        df = pd.DataFrame(tables)

        # fmt:off
        df = pd.concat(
            [tables[0], tables[1], tables[2], tables[3], tables[4], tables[5], tables[6],]
        )

        # general: DataFrame = tables[0]
        # interior: DataFrame = tables[1]
        # exterior: DataFrame = tables[2]
        # facilities: DataFrame = tables[3]
        # energy: DataFrame = tables[4]
        # townPlanning: DataFrame = tables[5]
        # financial: DataFrame = tables[6]

        # put the sub data frame in a list to a easy acces in the loop
        # titles: List[DataFrame] = [
        #     general,
        #     interior,
        #     exterior,
        #     facilities,
        #     energy,
        #     townPlanning,
        #     financial,
        # ]

        for _, v in df.iterrows():
            if v[0] in self.list_asked:
                key = v[0]
                value = v[1]

                for item in self.list_asked:
                    if key == item:
                        self.output[key].append(value)

        #### Fill empty column

        #         if key == item:

        #             self.output[key] = value

        # for title in titles:

        # # for firstColumn, secondColumn in title.iterrows():

        #     key = secondColumn[0]
        #     value = secondColumn[1]

        #     for item in self.list_asked:

        #         if key == item:

        #             self.output[key] = value

        return self.output


if __name__ == "__main__":
    dealer = Cleaner()

    url = "https://www.immoweb.be/en/classified/town-house/for-sale/laeken/1020/9730456?searchId=61f79f25891ae"
    result = dealer.getData(url)
    print(result)
