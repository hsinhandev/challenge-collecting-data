import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
import re
import selenium
from selenium.webdriver.firefox.webdriver import WebDriver
from typing import List
from selenium.webdriver.common.by import By
from pandas import DataFrame
from pandas import read_html
import concurrent.futures
from functools import reduce

class Cleaner:
      
    def __init__(self):
            
        self.links = pd.read_csv("./data/links.csv")['link']



    def getData(self,url) -> dict:
        """
        to get all the data we need that we can found in the web table
        """

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

        myData:dict = {}

        regex:str = "[^\/]+"

        dividedUrl:List[str] = re.findall(regex,url)

        subtypeOfProperty:str = dividedUrl[4]

        locality:str = dividedUrl[6] + " " + dividedUrl[7]

        myData["Subtype of property"] = subtypeOfProperty

        myData["Locality"] = locality


        response = requests.get(url)

        soup = BeautifulSoup(response.content, "lxml")

        soup2 = soup.prettify

        myContent = soup.find_all("tr")

        regexHeader = "(?:<th.+>)(.+)(?:</th>)"

        #regexData = "(?!<td.+>)(?!\s{2,})(\w+)(?!<[/]?span)"
        regexDataMinusTag = "<.+?>"
        regexDataMinusSpace = "\s{2,}"
        regexData = "[^\s]+?.+[^\s]+?"

        for i,line in enumerate(myContent):

            header = line.find("th")

            data =  line.find("td")


            if header != None:

                sortedHeader = re.findall(regexHeader, str(header))
                sortedData = re.sub(regexDataMinusSpace,"",str(data))
                sortedData = re.sub(regexDataMinusTag,"",sortedData)
                sortedData = re.findall(regexData,sortedData)

                if sortedHeader != []:
                
                    if sortedData == []:

                        sortedData.append(None)
                    
                    for key in listAsked:

                        if key == sortedHeader[0]:
                            
                            myData[key] = sortedData[0]

        return myData


        
    def concurrent(self):
        print(self.links[0])
        with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(self.getData, self.links[0])


