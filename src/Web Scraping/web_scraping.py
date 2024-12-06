import json
import re
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


# title, author, years, institution, location, keyword
class WebScraping:
    def __init__(self):
        # scrape_site(self):
        self.delay = 60

        # calculate_loop(self):
        self.start = 10000000
        self.end = 10700000
        self.num_iterations = 1000

        # get_browser(self):
        self.html = None
        self.browser = None

    # Generate a list of evenly spaced values from Start to End with Num_iterations steps.
    def calculate_loop(self):
        step = (self.end - self.start) // self.num_iterations
        self.doc_id_list = [self.start + i * step for i in range(self.num_iterations)]

    # Create link to be turned into soups
    def create_url(self, doc_id):
        return f"https://ieeexplore.ieee.org/document/{doc_id}"

    # Turns links into soups
    def soupify(self, url):
        # Trick sites to allow us to scrape
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0 Safari/537.36"
        }
        try:
            response = requests.get(url, headers=headers, timeout=10)
            html = response.text
            soup = BeautifulSoup(html, "lxml")
            return soup
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch URL {url}: {e}")
            return None

    def get_browser(self, doc_id):
        url = self.create_url(doc_id=doc_id)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--window-size=1920,1080")
        self.browser = webdriver.Chrome(options=chrome_options)
        self.browser.get(url)
        self.html = self.browser.execute_script(
            "return document.documentElement.outerHTML"
        )
        # self.html[:3000]
        time.sleep(3)
        return self.browser


def scrape_site():
    scraper = WebScraping()
    """
    # for doc_id in scraper.doc_id_list:
    for doc_id in range(10000000, 10000001):
        url = scraper.create_url(doc_id=doc_id, type="a")
        soup = scraper.soupify(url)

        if soup:
            # TODO Do something if we can get the soup ...
            print(url)
            print(
                soup.title.string.split("|")[0].strip()
                if soup.title
                else "No title found"
            )
        else:
            print(f"Skipping Document ID: {doc_id} due to an error.")

        # Rate Limiting
        # time.sleep(scraper.delay)
    """

    for doc_id in range(10000000, 10000001):
        browser = scraper.get_browser(doc_id)

        # press author button
        authors_button = browser.find_element(By.ID, "authors")
        authors_button.click()
        browser.implicitly_wait(5)

        # Extract and print author names
        author_elements = browser.find_elements(
            By.XPATH, "//div[contains(@class, 'author-card')]//a/span"
        )
        author_names = [
            author.text for author in author_elements if author.text.strip() != ""
        ]
        print("Author names found:", author_names)

        # time.sleep(scraper.delay)
        browser.quit()


start_time = time.time()
print("Start scraping! ==================================================")

scrape_site()

end_time = time.time()
elapsed_time = end_time - start_time
print(f"\nTime taken: {elapsed_time:.2f} seconds")
