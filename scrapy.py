import requests # type: ignore
import pandas as pd # type: ignore
from bs4 import BeautifulSoup

def scrape_amazon():
    url = "https://www.amazon.com/s?i=specialty-aps&bbn=16225007011&rh=n%3A16225007011%2Cn%3A1292115011&refresh=2&ref=glow_cls"
    custom_headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'accept-language': 'en-GB, en:q=0.9'
    } 
    page = requests.get(url, headers=custom_headers)

    soup = BeautifulSoup(page.text, "lxml")

    print(soup)

if __name__ == "__main__":
    scrape_amazon()
