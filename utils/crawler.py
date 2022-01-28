from typing import List, Dict
import re
import selenium
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.options import Options


def extract_property_link(num_pages: int) -> List[str]:
    """[Extrat property link from websites]

    Args:
        num_pages (int): [pages index]

    Returns:
        [type]: [List[str]]
    """

    print(f"====== Collection pages {num_pages}")

    # elissa_url = "https://immoelissa.be/immobilier/?sort=prix-c"
    elissa_url_pages = f"https://immoelissa.be/immobilier/?pg={num_pages}&sort=prix-c"

    # =================================================================init
    service = Service("./vendor/geckodriver")
    firefox_options = Options()
    # TODO debug
    firefox_options.add_argument("--headless")  # Ensure GUI is off
    browser = webdriver.Firefox(service=service, options=firefox_options)

    browser.get(elissa_url_pages)

    # browser.implicitly_wait(1)

    html = browser.page_source
    soup = BeautifulSoup(html, "lxml")

    browser.close()

    links = []
    for card in soup.select("div.results-view .lf-item>a"):
        property_link = card.get("href")
        links.append(property_link)

    print(f"====== Collection pages {num_pages} Finished =======")
    return links


def get_property_link_until_thousnad() -> Dict[str, str]:
    """[This function should call extract_property_link 1000 times, to get all the property link]

    Returns:
        [type]: [description]
    """
    properties_link = {"link": []}

    for num in range(1, 5):
        for href in extract_property_link(num):
            properties_link["link"].append(href)

    return properties_link


if __name__ == "__main__":
    property_link_output = get_property_link_until_thousnad()
    df = pd.DataFrame(property_link_output)
    df.to_csv(r"./data/property_link.csv", index=False, header=True)
