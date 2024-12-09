import time

import pandas as pd


def drop_dupes():
    data = pd.read_csv(
        "C:/Users/ASUS/Desktop/Thames Work/Data Science Project 2024/New CSV/combined_output.csv"
    )
    data_cleaned = data.drop_duplicates(subset=["Title"])
    data_cleaned.to_csv(
        "C:/Users/ASUS/Desktop/Thames Work/Data Science Project 2024/New CSV/no_dupes.csv",
        index=False,
    )
    print("Duplicates removed, cleaned file saved as 'cleaned_file.csv'")


start_time = time.time()

drop_dupes()

end_time = time.time()
elapsed_time = end_time - start_time
print(f"\nTime taken: {elapsed_time:.2f} seconds")
