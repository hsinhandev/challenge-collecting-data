from utils.cleaner import Cleaner
from utils.crawler import Crawler
import time

url = "https://www.immoweb.be/en/classified/town-house/for-sale/laeken/1020/9730456?searchId=61f79f25891ae"



test = Cleaner()
print(test.getData(url))
