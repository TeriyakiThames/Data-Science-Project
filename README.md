# Data Science Project

## Data Prep:
1. change_extension.py <br />
• Run `change_extension.py` to turn the given Scorpus data into `.json` files.

2. data_extraction.py <br />
• Run `data_extraction.py` to loop through each year of the Scorpus data set and combine it into 1 single file while removing unncessary data.

3. impute_missing_value.py <br />
• After extracting data, run `impute_missing_value.py` to impute any missing values in the dataset.

## Web Scraping:
4. web_scraping.py <br />
• Run `main.py` to start scraping from [IEEExplore](https://ieeexplore.ieee.org/).
• Do note that the script will sometimes have `null` in the date field as it can't be found in some documents.
• For other missing values, the script will not save the file.
