from typing import List, Dict
from bs4 import BeautifulSoup
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

from concurrent.futures import ThreadPoolExecutor
import time

# TODO use closure to create browser
# =================================================================init
service = Service("./vendor/geckodriver")
firefox_options = Options()
# TODO debug
firefox_options.add_argument("--headless")  # Ensure GUI is off
browser = webdriver.Firefox(service=service, options=firefox_options)
browser.minimize_window()


def extract_property_link(num_pages: int) -> List[str]:
    """[Extrat property link from websites]

    Args:
        num_pages (int): [pages index]

    Returns:
        [type]: [List[str]]
    """

    print(f"====== Collection pages {num_pages}")

    immoweb_url_page = f"https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&page={num_pages}&orderBy=relevance"
    browser.get(immoweb_url_page)

    # Not working here??
    browser.implicitly_wait(10)

    property_list = browser.find_elements(By.CSS_SELECTOR, "ul#main-content article a")
    property_link = []
    for link in property_list:
        property_link.append(link.get_attribute("href"))

    print(f"====== Collection pages {num_pages} Finished =======")
    return property_link


if __name__ == "__main__":
    start = time.perf_counter()

    futures = []
    property_link_output = {"links": []}

    with ThreadPoolExecutor(max_workers=10) as ex:

        # page = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        # f1 = ex.map(extract_property_link, page)

        for idx in range(1, 10):
            futures.append(ex.submit(extract_property_link, idx))

        for future in futures:
            for link in future.result():
                property_link_output["links"].append(link)
        # browser.close()

        end = time.perf_counter()

        browser.close()
        print(property_link_output)
        # print("quit browser")

        df = pd.DataFrame(property_link_output)
        df.to_csv(r"./data/property_link.csv", index=False, header=True)

    print(f"How long does it take: {round(end - start, 2)}")
