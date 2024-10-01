import requests # type: ignore
import time
import pandas as pd # type: ignore
from bs4 import BeautifulSoup


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 


service = Service(executable_path="./chromedriver")
driver = webdriver.Chrome(service=service)
url = "https://www.amazon.com/s?i=computers-intl-ship&bbn=16225007011&rh=n%3A1292115011&dc&ds=v1%3AsYkCBCl%2Bka9plXFHMRFlkzFuPcELKHQ9Vt7AQ2GjoiY&qid=1727780297&refresh=2&rnid=85457740011&ref=sr_nr_p_123_1"


def scrape_amazon():
    page_class_name = "sg-col-20-of-24"
    div_class_name = "sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16"
    title_xpath = '//div[contains(@class, "sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16")]'


    tiltle_div_class_name = "a-section a-spacing-none a-spacing-top-small s-title-instructions-style"
    title_class_name = "a-size-mini"

    item_name_xpath = '//span[contains(@class, "a-size-base-plus a-color-base a-text-normal")]'
    
    rating_score_xpath = '//span[contains(@class, "a-icon-alt")]'
    rating_count_xpath = '//span[contains(@class, "a-size-base s-underline-text")]'

    review_div_class_name = "a-section a-spacing-none a-spacing-top-micro"
    review_span_class_name_rating = "a-icon-alt"
    review_span_class_name_count = "a-size-base s-underline-text"

    price_div_class_name = "a-section a-spacing-none a-spacing-top-small s-price-instructions-style"
    top_span_class_name = "a-price"
    price_span_class_name = "a-offscreen"

    seller_rating_div_name = "a-section a-spacing-none a-spacing-top-mini"
    seller_rating_span_class_name = "a-color-base"


    driver.get(url)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, page_class_name))
    )
    
    page = driver.page_source  # Get the source code of the page

    soup = BeautifulSoup(page, "html.parser")

    span_element = soup.find('span', class_=title_class_name)
    # print(span_element.text if span_element else "Element not found")
    items = []
    
    elements = driver.find_elements(By.XPATH, title_xpath)
    for element in elements:
        # Find the title, rating score, and rating count within the current element
        title = element.find_element(By.CLASS_NAME, title_class_name).text.split(",")
        # rating_score = element.find_element(By.XPATH, rating_score_xpath).text
        # rating_count = element.find_element(By.XPATH, rating_count_xpath).text

        # Append the extracted data to the items list
        items.append((title))
        print(element)

        time.sleep(2)
    
    print(items)

    driver.quit()

if __name__ == "__main__":
    scrape_amazon()
