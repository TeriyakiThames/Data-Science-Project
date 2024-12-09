import ast
import time

import pandas as pd
from geopy.geocoders import Nominatim


def load_dataset():
    file_path = "C:/Users/ASUS/Desktop/Thames Work/Data Science Project 2024/New CSV/no_dupes.csv"
    try:
        data = pd.read_csv(file_path, on_bad_lines="warn")
        return data
    except Exception as e:
        return pd.DataFrame()


def get_country_coordinates(country_name):
    try:
        geolocator = Nominatim(user_agent="country_geocoder")
        location = geolocator.geocode(country_name)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        return None, None


def calculate_map(df_dataset, output_filename="country_frequency.csv"):
    df = df_dataset
    df["Country"] = df["Country"].apply(ast.literal_eval)
    country_list = [country for sublist in df["Country"] for country in sublist]
    country_freq = pd.Series(country_list).value_counts().reset_index()
    country_freq.columns = ["country", "frequency"]
    country_freq["coordinates"] = country_freq["country"].apply(get_country_coordinates)
    country_freq = country_freq[
        country_freq["coordinates"].apply(lambda x: x != (None, None))
    ]
    country_freq["latitude"] = country_freq["coordinates"].apply(lambda x: x[0])
    country_freq["longitude"] = country_freq["coordinates"].apply(lambda x: x[1])

    # Save to CSV
    country_freq.to_csv(output_filename, index=False)

    return country_freq


start_time = time.time()

calculate_map(
    load_dataset(),
    output_filename="C:/Users/ASUS/Desktop/Thames Work/Data Science Project 2024/New CSV/calculated_map_data.csv",
)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"/nTime taken: {elapsed_time:.2f} seconds")
