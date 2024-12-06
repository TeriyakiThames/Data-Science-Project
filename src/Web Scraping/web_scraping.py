import json
import re
import time

import requests
from bs4 import BeautifulSoup


# title, author, years, institution, location, keyword
class WebScraping:
    def __init__(self):
        # scrape_site(self):
        self.delay = 60

        # calculate_loop(self):
        self.start = 10000000
        self.end = 10700000
        self.num_iterations = 1000

    # Generate a list of evenly spaced values from Start to End with Num_iterations steps.
    def calculate_loop(self):
        step = (self.end - self.start) // self.num_iterations
        self.doc_id_list = [self.start + i * step for i in range(self.num_iterations)]

    # Create link to be turned into soups
    def create_url(self, doc_id, type):
        # Type A for infos about authors
        if type == "a":
            return f"https://ieeexplore.ieee.org/document/{doc_id}/authors#authors"
        # Type K for infos about keywords
        elif type == "k":
            return f"https://ieeexplore.ieee.org/document/{doc_id}/keywords#keywords"
        else:
            raise ValueError("Invalid type specified. Use 'a' or 'k'.")

    # Turns links into soups
    def get_soup(self, url):
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


def scrape_site():
    scraper = WebScraping()
    # Generate URL N times
    for doc_id in scraper.doc_id_list:
        url = scraper.create_url(doc_id=doc_id, type="a")
        soup = scraper.get_soup(url)

        if soup:
            # TODO Do something if we can get the soup ...
            pass
        else:
            print(f"Skipping Document ID: {doc_id} due to an error.")

        # Rate Limiting
        time.sleep(scraper.delay)
