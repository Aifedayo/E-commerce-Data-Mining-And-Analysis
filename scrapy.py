import requests # type: ignore
import pandas as pd # type: ignore
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service


service = Service(excutable_path="./chromedriver")
driver = webdriver.Chrome(service=service)

def scrape_amazon():
    url = "https://www.amazon.com/s?i=computers-intl-ship&bbn=16225007011&rh=n%3A1292115011&dc&ds=v1%3AsYkCBCl%2Bka9plXFHMRFlkzFuPcELKHQ9Vt7AQ2GjoiY&qid=1727780297&refresh=2&rnid=85457740011&ref=sr_nr_p_123_1"
    
    custom_headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'accept-language': 'en-GB, en:q=0.9'
    } 
    driver.get(url)

    page = driver.page_source  # Get the source code of the page

    soup = BeautifulSoup(page.text, "html.parser")

    span_element = soup.find('span', class_='a-size-base-plus a-color-base a-text-normal')
    print(span_element.text if span_element else "Element not found")

    driver.quit()

if __name__ == "__main__":
    scrape_amazon()
