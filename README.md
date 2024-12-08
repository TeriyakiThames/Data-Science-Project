# Data Science Project

## Data Prep:
0. `main.py` <br />
• Running this file will automatically run all the other files in `Data Prep`. <br />
• Input the starting folder (the root folder of the dataset), the folder you want to extract the data to, and the folder you want to store the imputed data.

2. `change_extension.py` <br />
• This file turns the given Scorpus dataset into `.json` files.

3. `data_extraction.py` <br />
• This file loops through each year of the Scorpus data set and combine it into 1 single file while removing unncessary data.

4. `impute_missing_value.py` <br />
• This file imputes any missing values in the dataset.

## Web Scraping:
0. `main.py` <br />
• Use this file to run `web_scraping.py`

1. `web_scraping.py` <br />
• Run `main.py` to start scraping from [IEEExplore](https://ieeexplore.ieee.org/). <br />
• Do note that the script will sometimes have `null` in the date field as it can't be found in some documents. <br />
• For other missing values, the script will not save the file. <br />

2. `join_json.py` <br />
• This file is used to join the json files obtained from web scraping into one file. <br />
• You can then use the result of this function to impute the missing values using `impute_missing_value.py`.
