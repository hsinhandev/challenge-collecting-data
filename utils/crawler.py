from typing import List, Dict
from bs4 import BeautifulSoup
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

# TODO use closure to create browser
# =================================================================init
service = Service("./vendor/geckodriver")
firefox_options = Options()
# TODO debug
# firefox_options.add_argument("--headless")  # Ensure GUI is off
browser = webdriver.Firefox(service=service, options=firefox_options)


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


def get_property_link_until_ten_thousnad() -> Dict[str, str]:
    """[This function should call extract_property_link until 10,000 property link]

    Returns:
        [type]: [description]
    """
    properties_link = {"link": []}

    # TODO fix crash at page 12
    for num in range(1, 100):
        for href in extract_property_link(num):
            properties_link["link"].append(href)
    return properties_link


if __name__ == "__main__":
    try:
        property_link_output = get_property_link_until_ten_thousnad()
        df = pd.DataFrame(property_link_output)
        df.to_csv(r"./data/property_link.csv", index=False, header=True)
    except NoSuchElementException:
        time.sleep(2)
    except TimeoutException as ex:
        print(ex.message)
    finally:
        browser.quit()
