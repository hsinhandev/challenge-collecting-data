# import bs4
import requests
from bs4 import BeautifulSoup
# import numpy as np
import pandas as pd
# import re
import os
from pandas import DataFrame
from pandas import read_html 
from typing import List

def extract_property_info():
    """[Extract infomation from each property]"""

    property_csv_path = os.path.join(os.path.dirname(__file__), "../data/property_link.csv")

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

        
def getData(url):
    """ To get Data asked from website """

    url = "https://www.immoweb.be/en/classified/apartment-block/for-sale/berchem-sainte-agathe/1082/9711185?searchId=61f7dcf790a32"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")

    soup2 = soup.prettify()
    tables:DataFrame  = pd.read_html(soup2)         # To get tabels from website

    # create a list of all tables 
    titles:List[DataFrame] = [tables[0], tables[1], tables[2], tables[3], tables[4], tables[5], tables[6]]

    #a list of everything that the exercice asked
    listAsked:List[str] = [
                "Price",
                "Neighbourhood or locality"
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

    #My required data will be stored in myData in dictionary
    myData:dict = {}

    for title in titles:
        for _ ,secondColumn in title.iterrows():

            key = secondColumn[0]
            value = secondColumn[1]

            for item in listAsked:

                if key == item:

                    myData[key] = value
                    if value == None:
                        myData[key] = None

    print(myData)