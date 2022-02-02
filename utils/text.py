from asyncio.base_subprocess import BaseSubprocessTransport
from threading import local
import requests
from bs4 import BeautifulSoup
import lxml
import re
from selenium.webdriver.firefox.webdriver import WebDriver
import selenium
from selenium.webdriver.common.by import By



url = "https://www.immoweb.be/en/classified/town-house/for-sale/laeken/1020/9730456?searchId=61f79f25891ae"

response = requests.get(url)

soup = BeautifulSoup(response.content, "lxml")

locality = soup.select(".classified__information--address-row span")

print("locality printing")

print(locality)

for i in locality:
    print("lol")
    print(i)
    #print(elem)