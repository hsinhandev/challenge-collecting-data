from asyncio.base_subprocess import BaseSubprocessTransport
from threading import local
from urllib import response
import requests
from bs4 import BeautifulSoup
import lxml
import re
from selenium.webdriver.firefox.webdriver import WebDriver
import selenium
from selenium.webdriver.common.by import By
import time
from typing import List
from pandas import DataFrame, read_html



url = "https://www.immoweb.be/en/classified/town-house/for-sale/laeken/1020/9730456?searchId=61f79f25891ae"

regex = "[^\/]+"

dividedUrl = re.findall(regex,url)

subtypeOfProperty = dividedUrl[4]

locality = dividedUrl[6] + " " + dividedUrl[7]
