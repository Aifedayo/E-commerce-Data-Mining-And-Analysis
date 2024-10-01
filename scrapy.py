import time
import pprint
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup Selenium WebDriver
service = Service(executable_path="./chromedriver")
driver = webdriver.Chrome(service=service)

# Amazon URL
url = "https://www.amazon.com/s?i=computers-intl-ship&bbn=16225007011&rh=n%3A1292115011&dc&ds=v1%3AsYkCBCl%2Bka9plXFHMRFlkzFuPcELKHQ9Vt7AQ2GjoiY&qid=1727780297&refresh=2&rnid=85457740011&ref=sr_nr_p_123_1"
printer = pprint.PrettyPrinter()

def scrape_amazon():
    page_class_name = "sg-col-20-of-24"
    title_xpath = '//div[contains(@class, "sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16")]'

    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, page_class_name))
    )
    
    page = driver.page_source  # Get the source code of the page

    soup = BeautifulSoup(page, "html.parser")

    driver.get(url)

    title_spans = [span.text for span in soup.find_all('h2', class_="a-size-mini a-spacing-none a-color-base s-line-clamp-4")]
    rating_score_spans = [span.text for span in soup.find_all("span", class_="a-icon-alt")]
    rating_count_spans = [span.text for span in soup.find_all("span", class_="a-size-base s-underline-text")]
    price_spans = [ nested_span.text if nested_span else "0.0"
                   for price_span in soup.find_all("span", class_="a-price")
                   for nested_span in price_span.find_all("span", class_="a-offscreen")]

    rating_div = soup.find_all("div", "a-section a-spacing-none a-spacing-top-mini")
    seller_rating_score = [span.text for span in rating_div.find_all("span", class_="a-color-base")]

    print(seller_rating_score)


    items = []
    
    elements = driver.find_elements(By.XPATH, title_xpath)
    for i, element in enumerate(elements):
        # Find the title, rating score, and rating count within the current element
        title = title_spans[i] if i < len(title_spans) else "No title"
        rating_score = rating_score_spans[i] if i < len(rating_score_spans) else "No rating"
        rating_count = rating_count_spans[i] if i < len(rating_count_spans) else 0
        price = price_spans[i] if i < len(price_spans) else 0.0
        seller_rating_score = seller_rating_score[i] if i < len(seller_rating_score) else "No rating"
        # seller_rating_count = seller_rating_count[i] if i < len(seller_rating_count) else 0


        # Append the extracted data to the items list
        items.append((title, rating_score, rating_count, price, seller_rating_score))
    
    printer.pprint(items)

    driver.quit()

if __name__ == "__main__":
    scrape_amazon()