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
    driver.get(url)

    page_class_name = "sg-col-20-of-24"
    title_xpath = '//div[contains(@class, "sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16")]'

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, page_class_name))
    )

    for i in range(7):
        # Wait until the 'brandsRefinements' section is loaded
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@id, 'brandsRefinements')]"))
        )
        model_checkbox_element = driver.find_element(By.XPATH, "//div[contains(@id, 'brandsRefinements')]")
        ul_element = model_checkbox_element.find_element(By.XPATH, "(//ul[contains(@class, 'a-unordered-list')])[1]")

        span_element = ul_element.find_element(By.CLASS_NAME, 'a-declarative')

        checkbox = span_element.find_elements(By.XPATH, "//i[@class='a-icon a-icon-checkbox']")[i]

        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(checkbox)
        )
        if not checkbox.is_selected():
            checkbox.click()
        # All checkboxes selected :::
    
    items = {
        "name": [],
        "rating_score": [],
        "rating_count": [],
        "pieces_sold": [],
        "price": []
    }

    while True:

        """START GRABBING THE ITEMS YOU NEED"""
        # Wait for the page to update after interacting with checkboxes
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//h2[@class='a-size-mini a-spacing-none a-color-base s-line-clamp-4']"))
        )

        page = driver.page_source  # Get the source code of the page
        soup = BeautifulSoup(page, "html.parser")

        title_spans = [span.text.split(',')[0].strip() for span in soup.find_all('h2', class_="a-size-mini a-spacing-none a-color-base s-line-clamp-4")]
        rating_score_spans = [span.text for span in soup.find_all("span", class_="a-icon-alt")]
        rating_count_spans = [span.text for span in soup.find_all("span", class_="a-size-base s-underline-text")]
        pieces_sold_spans = [nested_span.text if nested_span else 0 
                            for pieces_span in soup.find_all("div", "a-row a-size-base")
                            for nested_span in pieces_span.find_all("span", class_="a-size-base a-color-secondary")]
        price_spans = [ nested_span.text if nested_span else "0.0"
                    for price_span in soup.find_all("span", class_="a-price")
                    for nested_span in price_span.find_all("span", class_="a-offscreen")]
        
        # # Print titles for debugging
        # print(f"Extracted Titles: {title_spans}")
        
        elements = driver.find_elements(By.XPATH, title_xpath)

        num_elements = min(len(elements), len(title_spans), len(rating_score_spans), len(rating_count_spans), len(pieces_sold_spans), len(price_spans))

        for i in range(num_elements):
            # Append the data directly to the lists in the items dictionary
            items["name"].append(title_spans[i] if title_spans[i] else "No title")
            items["rating_score"].append(rating_score_spans[i] if rating_score_spans[i] else "No rating")
            items["rating_count"].append(rating_count_spans[i] if rating_count_spans[i] else 0)
            items["pieces_sold"].append(pieces_sold_spans[i] if pieces_sold_spans[i] else "Zero bought")
            items["price"].append(price_spans[i] if price_spans[i] else 0.0)

        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Next')]"))
            ).click()

            # Wait for the new page to load after clicking "Next"
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, title_xpath))
            )
        
        except Exception as e:
            print("No more pages or unable to find 'Next' button.")
            break
    
    df = pd.DataFrame.from_dict(items)
    
    # Export to csv
    df.to_csv('amazon_monitors_scraped_data.csv', index=False)
    return items

    # driver.quit()

if __name__ == "__main__":
    scrape_amazon()