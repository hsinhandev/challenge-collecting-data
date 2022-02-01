import os
import logging
import pandas as pd
import requests
from urllib import parse
from bs4 import BeautifulSoup
import constants
from typing import List, Dict


def csv_to_list() -> List[str]:
    links = None
    try:
        property_csv_path = os.path.join(
            os.path.dirname(__file__), "../data/property_link.csv"
        )
        df = pd.read_csv(property_csv_path)
        links = df.links.to_list()
    except IOError as e:
        logging.exception("")
    if not links:
        raise ValueError("No data available")
    return links


def extract_property_info(url: str):
    """[Extract infomation from each property]"""
    # OUTPUT comese from main

    html = requests.get(url)

    if html.ok:
        soup = BeautifulSoup(html.content, "lxml")

        parsed_url = parse.urlsplit(url).path.split("/")
        property_type = parse_property_type(parsed_url[3])
        output["property_type"].append(property_type)
        output["subtype_of_property"].append(parsed_url[3])
        output["locality"].append(parsed_url[5].replace("-", " "))

        return output

    raise Exception("Could not parse")


def parse_property_type(t: str) -> str:
    """[parse url and return house type]"""
    if any(st in t for st in constants.APARTMENT_TYPE):
        return "apartment"
    return "house"


if __name__ == "__main__":
    output: Dict[str, List[str]] = {k: [] for k in constants.TARGET_ATTRS}
    property_links = csv_to_list()

    extract_property_info(property_links[3])
    print(output)
