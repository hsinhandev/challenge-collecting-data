import os
import lxml
import requests
import pandas as pd
from csv import reader
from bs4 import BeautifulSoup

links = []

csv_path = os.path.abspath("data/links.csv")

with open(csv_path, 'r') as file:
    csv_reader = reader(file)
    for row in csv_reader:
        links.append(row[0])

def get_data(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, "lxml")

    container = soup.find("dl", attrs={"class": "tab-content listing-tabs"})
    print(container.find('h5'))

for link in links:
    get_data(link)
    break

target_attributes = (
    "Locality",
    "Type of property",
    "Subtype of property",
    "Price",
    "Type of sale",
    "Number of rooms",
    "Area",
    "State of the building " "Surface of the land",
    "Surface area of the plot of land",
    "Number of facades",
    "Swimming pool",
    "Fully equipped kitchen",
    "Furnished",
    "Open fire ",
    "Terrace",
    "Garden",
)

target_attributes_FR = (
    "Locality",
    "Type du bien",
    "Subtype of property",
    "Prix",
    "Disponibilité",
    "Number of rooms",
    "Ville",
    "État du bien",
    "Surface of the land",
    "Surface area of the plot of land",
    "Number of facades",
    "Swimming pool",
    "Fully equipped kitchen",
    "Furnished",
    "Open fire ",
    "Terrace",
    "Garden",
)