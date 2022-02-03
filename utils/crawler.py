import time
import random
import concurrent.futures
from tracemalloc import start
from typing import List,Dict
from unittest import result

import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

class Crawler:

    def __init__(self) -> None:
        self.links = []



    def countForMe(funct):

        def inner(*args, **kwargs):

            widthOfScreen = 150

            print("-"*widthOfScreen)

            print(f"Test - count the time that the function '{funct.__name__}' take to be executed :")

            print("-"*widthOfScreen)

            start = time.perf_counter()

            funct(*args, **kwargs)
            
            end = time.perf_counter()

            final = round(end-start,3)

            print("-"*widthOfScreen)

            print(f"the time that the function '{funct.__name__}' took is '{final}' sec")

            print("-"*widthOfScreen)
            print("-"*widthOfScreen)

            return final

        
        return inner



    def get_all_Links(self,page_num) -> List[str]:
        """Function:- Find all links for house and apartment"""
        
        url = f"https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&page={page_num}&orderBy=relevance"

        #options = webdriver.ChromeOptions()
        #options.add_argument('headless')
        driver = webdriver.Chrome()
        # Here, we create instance of Chrome WebDriver.
        driver.get(url)

        elem = driver.find_elements(By.CSS_SELECTOR, 'ul#main-content article a')
        for link in elem:
            self.links.append(link.get_attribute('href'))

        driver.quit()

        return self.links    

    @countForMe
    def concurrents(self,numOfPage) -> None:

        with concurrent.futures.ThreadPoolExecutor() as executor:
            """Run concurrently using Threading module and collect link
            for every the pages mentioned in the list"""
            #func = all_pages(get_all_Links)
            page = [i for i in range(numOfPage)]
            f1 = executor.map(self.get_all_Links, page)

            for elem in f1:
                self.links.append(elem)


    def simpleWay(self,numOfPage) ->None:

       
        f1 = self.get_all_Links(numOfPage)

        for elem in f1:
            self.links.append(elem)


    def writeIt(self) -> None :

        df = pd.DataFrame(dict(link = self.links))
        df.to_csv(r"./data/links.csv", index=False, header=True)



    



        