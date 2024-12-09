import json
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# title, author, years, institution, location, keyword
class WebScraping:
    def __init__(self):
        # scrape_site(self):
        self.delay = 2

        # calculate_loop(self):
        self.start = 10350001
        self.end = 10700001
        self.num_iterations = 444

        # get_browser(self):
        self.html = None
        self.browser = None

    # Generate a list of evenly spaced values from Start to End with Num_iterations steps.
    def calculate_loop(self):
        step = (self.end - self.start) // self.num_iterations
        self.doc_id_list = [self.start + i * step for i in range(self.num_iterations)]
        self.doc_id_list = self.doc_id_list[::-1]

    # Create link to be turned into soups
    def create_url(self, doc_id):
        return f"https://ieeexplore.ieee.org/document/{doc_id}"

    def get_browser(self, doc_id):
        url = self.create_url(doc_id=doc_id)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--window-size=1920,1080")
        self.browser = webdriver.Chrome(options=chrome_options)
        self.browser.get(url)
        self.html = self.browser.execute_script(
            "return document.documentElement.outerHTML"
        )
        return self.browser

    def click_cookies(self, browser):
        try:
            consent_button = WebDriverWait(browser, self.delay).until(
                EC.element_to_be_clickable((By.ID, "cookieConsentButtonID"))
            )
            consent_button.click()
        except:
            # print("Cookie consent button not found or not needed.")
            pass

    def find_title(self, browser):
        try:
            title_element = browser.find_element(
                By.XPATH, "//h1[contains(@class, 'document-title')]//span"
            )
            title = title_element.text.strip()
            return title
        except Exception as e:
            print("Error extracting title:", e)

    def find_date(self, browser):
        try:
            date_added_element = browser.find_element(
                By.XPATH, "//div[contains(@class, 'doc-abstract-dateadded')]"
            )
            # Extract the date string
            string_date = " ".join(date_added_element.text.strip().split()[-3:])

            # Parse the date string and convert it to the required format
            date_object = datetime.strptime(
                string_date, "%d %B %Y"
            )  # "09 January 2023"
            formatted_date = date_object.strftime("%Y-%m-%d")  # "2023-01-09"

            return formatted_date
        except Exception as e:
            print("Error extracting date:", e)

    def find_author_institution_location(self, browser):
        authors = self.__find_authors(browser)
        institution = self.__find_institution_and_location(browser)
        return authors, institution

    def __find_authors(self, browser):
        try:
            # Find and click the authors button
            authors_button = WebDriverWait(browser, self.delay).until(
                EC.element_to_be_clickable((By.ID, "authors"))
            )
            browser.execute_script("arguments[0].scrollIntoView(true);", authors_button)
            authors_button.click()
            browser.implicitly_wait(self.delay)

            # Scrape authors
            author_elements = browser.find_elements(
                By.XPATH, "//div[contains(@class, 'author-card')]//a/span"
            )
            author_names = [
                author.text for author in author_elements if author.text.strip() != ""
            ]
            return author_names
        except Exception as e:
            print("Error extracting authors:", e)

    def __find_institution_and_location(self, browser):
        try:
            # Find the institution and add it to a list
            institution_elements = browser.find_elements(
                By.XPATH, "//div[contains(@class, 'author-card')]//div[not(@class)]"
            )
            seen_institutions = set()
            institution_texts = [
                institution.text.strip()
                for i, institution in enumerate(institution_elements)
                if institution.text.strip()
                and i % 2 != 0
                and institution.text.strip() not in seen_institutions
                and not seen_institutions.add(institution.text.strip())
            ]

            # Split the text of each institution information to country, city, and institution
            institution, city, country = zip(
                *[
                    tuple(map(str.strip, object.split(",")[-3:]))
                    for object in institution_texts
                ]
            )
            country = list(set(country))
            city = list(set(city))
            institution = list(set(institution))

            return country, city, institution

        except Exception as e:
            print("Error extracting institution/organization:", e)

    def find_keyword(self, browser):
        try:
            # Find and click the keywords button
            keywords_button = WebDriverWait(browser, self.delay).until(
                EC.element_to_be_clickable((By.ID, "keywords"))
            )
            browser.execute_script(
                "arguments[0].scrollIntoView(true);", keywords_button
            )
            keywords_button.click()

            # Scrape keywords
            keywords_elements = browser.find_elements(
                By.XPATH,
                "//ul[contains(@class, 'List--no-style')]//a[contains(@class, 'stats-keywords-list-item')]",
            )
            keywords = [
                keyword.text.strip()
                for keyword in keywords_elements
                if keyword.text.strip()
            ]
            keywords = list(set(keywords))
            return keywords

        except Exception as e:
            print("Error while scraping keywords:", e)

    def pack_to_json(
        self, title, date, authors, country, city, institution, keywords, filename
    ):
        data = {
            "Title": title,
            "Authors": authors,
            "Date": date,
            "Institution": institution,
            "City": city,
            "Country": country,
            "Keywords": keywords,
        }

        # Write the data to the JSON file
        with open(filename, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

        print(f"Data saved to {filename}")
