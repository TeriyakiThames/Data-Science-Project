import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# title, author, years, institution, location, keyword
class WebScraping:
    def __init__(self):
        # scrape_site(self):
        self.delay = 60

        # calculate_loop(self):
        self.start = 10000000
        self.end = 10700000
        self.num_iterations = 1000
        self.doc_id_list = None

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

    def click_cookies(self, browser):
        try:
            consent_button = WebDriverWait(browser, 10).until(
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
            string_date = " ".join(date_added_element.text.strip().split()[-3:])
            return string_date
        except Exception as e:
            print("Error extracting date:", e)

    def find_author_institution_location(self, browser):
        authors = self.__find_authors(browser)
        institution = self.__find_institution_and_location(browser)
        return authors, institution

    def __find_authors(self, browser):
        try:
            # Find and click the authors button
            authors_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.ID, "authors"))
            )
            browser.execute_script("arguments[0].scrollIntoView(true);", authors_button)
            authors_button.click()
            browser.implicitly_wait(5)

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

            # Split the text of each institution information to country, city, and university
            university, city, country = zip(
                *[
                    tuple(map(str.strip, object.split(",")[-3:]))
                    for object in institution_texts
                ]
            )
            country = list(set(country))
            city = list(set(city))
            university = list(set(university))

            return country, city, university

        except Exception as e:
            print("Error extracting institution/organization:", e)

    def find_keyword(self, browser):
        try:
            # Find and click the keywords button
            keywords_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.ID, "keywords"))
            )
            browser.execute_script(
                "arguments[0].scrollIntoView(true);", keywords_button
            )
            keywords_button.click()
            time.sleep(2)

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
        self, title, date, authors, country, city, university, keywords, filename
    ):
        data = {
            "Title": title,
            "Date": date,
            "Authors": authors,
            "Country": country,
            "City": city,
            "University": university,
            "Keywords": keywords,
        }

        # Write the data to the JSON file
        with open(filename, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

        print(f"Data saved to {filename}")


def scrape_site():
    scraper = WebScraping()

    for doc_id in scraper.doc_id_list:
        # for doc_id in range(10000000, 10000002):
        browser = scraper.get_browser(doc_id)
        # Click cookies banner first if its in the way
        scraper.click_cookies(browser)

        # Scrape through information such as title, authors, year, institution, and location
        title = scraper.find_title(browser)
        date = scraper.find_date(browser)
        authors, country_city_university = scraper.find_author_institution_location(
            browser
        )
        country, city, university = country_city_university
        keywords = scraper.find_keyword(browser)

        # Print out the results of the scrape
        labels = [
            "Title",
            "Date",
            "Authors",
            "Country",
            "City",
            "University",
            "Keywords",
        ]
        values = [title, date, authors, country, city, university, keywords]
        print(
            f"\nResults of {doc_id}: =================================================="
        )
        for label, value in zip(labels, values):
            print(f"{label}: {value}")

        browser.quit()

        # Save data to json
        scraper.pack_to_json(
            title,
            date,
            authors,
            country,
            city,
            university,
            keywords,
            filename=f"C:/Users/ASUS/Desktop/Thames' Work/Data Science Project 2024/Web Scraping/{doc_id}.json",
        )

        # Rate Limiting
        time.sleep(scraper.delay)


start_time = time.time()
print("Start scraping! ==================================================")

scrape_site()

end_time = time.time()
elapsed_time = end_time - start_time
print(f"\nTime taken: {elapsed_time:.2f} seconds")
