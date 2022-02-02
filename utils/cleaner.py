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
    # OUTPUT comese from __main__

    html = requests.get(url)

    if html.ok:
        soup = BeautifulSoup(html.content, "lxml")

        parsed_url = parse.urlsplit(url).path.split("/")
        property_type = parse_property_type(parsed_url[3])
        output["property_type"].append(property_type)
        output["subtype_of_property"].append(parsed_url[3])
        output["locality"].append(parsed_url[5].replace("-", " "))

        attributes = soup.select("th.classified-table__header")

        for tag in attributes:
            if tag.string.strip() not in constants.TARGET_ATTRS:
                continue

            key = tag.string.strip()
            # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#string
            # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#contents-and-children
            # Read DOCUMENTATION!
            # Waste my time!!!!!
            value = tag.find_next("td").contents[0].strip()
            output[key].append(value)
            print(f"{key}: {value}")

        # fill empty columns
        for k in constants.TARGET_ATTRS_YES_NO:
            if not output[k]:
                output[k].append(0)
        for k in constants.TARGET_ATTRS:
            if not output[k]:
                output[k].append(None)

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

    extract_property_info(property_links[2])
    print(output)
