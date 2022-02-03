from typing import List, Dict
from bs4 import BeautifulSoup
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

from concurrent.futures import ProcessPoolExecutor
import time
from helper import kill_browser

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

    # futures = []
    property_link_output = {"links": []}

    with ProcessPoolExecutor(max_workers=10) as ex:
        futures = ex.map(extract_property_link, range(1, 334))
        # for idx in range(1, 10):
        #     futures.append(ex.submit(extract_property_link, idx))

        for future in futures:
            for link in future:
                property_link_output["links"].append(link)

        end = time.perf_counter()
        print(property_link_output)

        # browser.quit()
        kill_browser()

        df = pd.DataFrame(property_link_output)
        df.to_csv(r"./data/property_link.csv", index=False, header=True)

    print(f"How long does it take: {round(end - start, 2)}")
