from asyncio.base_subprocess import BaseSubprocessTransport
import requests
from bs4 import BeautifulSoup
import lxml
import re
from selenium.webdriver.firefox.webdriver import WebDriver
import selenium
from selenium.webdriver.common.by import By



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


