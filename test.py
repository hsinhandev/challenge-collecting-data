
from pandas import DataFrame
import pandas 
from bs4 import BeautifulSoup
import requests
import lxml
from typing import List
import re



url = "https://www.immoweb.be/en/classified/house/for-sale/evere/1140/9730623?searchId=61f93dee1b1bc"

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
            
print(myData)
    
