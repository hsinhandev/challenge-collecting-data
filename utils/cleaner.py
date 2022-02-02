import logging
from typing import Dict, List
from urllib import parse

import pandas as pd
import numpy as np

import requests
from bs4 import BeautifulSoup

import constants


def csv_to_list() -> List[str]:
    links = None
    try:
        df = pd.read_csv("./data/property_link.csv")
        links = df.links.to_list()
    except IOError as e:
        logging.exception("")
    if not links:
        raise ValueError("No data available")
    return links


def extract_property_info(url: str, idx: int):
    """[Extract infomation from each property]"""
    # OUTPUT comese from __main__

    html = requests.get(url)

    idx = idx + 1
    if html.ok:
        soup = BeautifulSoup(html.content, "lxml")

        parsed_url = parse.urlsplit(url).path.split("/")
        property_type = parse_property_type(parsed_url[3])
        output["property_type"].append(property_type)
        output["subtype_of_property"].append(parsed_url[3])
        output["Locality"].append(parsed_url[5].replace("-", " "))
        output["Postal_code"].append(parsed_url[6])
        output["price"].append(
            soup.select("p.classified__price span.sr-only")[0].string
        )

        attributes = soup.select("th.classified-table__header")

        for tag in attributes:
            if tag.string.strip() not in constants.TARGET_ATTRS:
                continue

            key = tag.string.strip()
            # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#string
            # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#contents-and-children
            # Read DOCUMENTATION! # Waste my time!!!!!
            value = tag.find_next("td").contents[0].strip()
            output[key].append(value)
            # print(f"{key}: {value}")

        # fill empty columns
        for k in constants.TARGET_ATTRS_YES_NO:
            if not output[k] or len(output[k]) != idx:
                output[k].append(0)
        for k in constants.TARGET_ATTRS:
            if not output[k] or len(output[k]) != idx:
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

    for idx, link in enumerate(property_links[0:15]):
        extract_property_info(link, idx)

    df = pd.DataFrame(output)
    # Data cleaning
    df["Kitchen type"] = np.where(df["Kitchen type"] != "Not installed", 1, 0)
    # clean YES/NO to 1/0
    for column in df:
        if column in constants.TARGET_ATTRS_YES_NO:
            df[column] = df[column].apply(lambda c: 0 if c == "No" else 1)

    df.to_csv("./data/property_info.csv")
