import time

from web_scraping import WebScraping


def scrape_site():
    scraper = WebScraping()

    # for doc_id in scraper.doc_id_list:
    for doc_id in range(10000000, 10000001):
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
