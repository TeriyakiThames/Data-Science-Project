# How do the affiliations of researchers influence the diversity of engineering research topics?

## Data Preparation:
0. `main.py` <br />
• Running this file will automatically run all the other files in `Data Prep`. <br />
• Input the starting folder (the root folder of the dataset), the folder you want to extract the data to, and the folder you want to store the imputed data.

2. `change_extension.py` <br />
• This file turns the given Scopus dataset into `.json` files.

3. `data_extraction.py` <br />
• This file loops through each year of the Scopus data set and combine it into 1 single file while removing unncessary data.

4. `impute_missing_value.py` <br />
• This file imputes any missing values in the dataset.

5. `remove_duplicates.py` <br / >
• This file will drop duplicated paper from the file.

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

## Model Training:
1. `Model.ipynb` <br />
• This file trains the model from the data collected from Scopus and from web scraping. <br />
• We used `Latent Dirichlet Allocation (LDA)` and `K Means`.

2. `combine_csv.py` <br />
• This file is used for combining all the CSV files together into 1 file.

## Data Visualisation
1. `data_visualisation.py` <br />
• This file visualises the data from Data Prep as well the model's fitted data. <br />
• The data is visualised using StreamLit. <br />
• There are 3 files which are used here (`main_data.csv`, `cluster_data.csv`, `calculated_map_data.csv`).

2. `calculate_map.py` <br />
• This file is originally in `data_visualisation.py`, but since it was too computationally heavy. <br />
• Therefore it was split off and the output is stored in a file to be loaded instead.
