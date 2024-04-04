import requests # type: ignore
import pandas as pd # type: ignore
from bs4 import BeautifulSoup

def scrape_amazon():
    url = "https://www.amazon.com/s?i=specialty-aps&bbn=16225007011&rh=n%3A16225007011%2Cn%3A1292115011&refresh=2&ref=glow_cls"
    page = requests.get(url)

    soup = BeautifulSoup(page.text, "html.parser")

    return soup

if __name__ == "__main__":
    scrape_amazon()
