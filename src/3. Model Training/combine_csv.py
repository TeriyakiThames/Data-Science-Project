import os

import pandas as pd

# Define the folder path where your CSV files are stored
folder_path = (
    "C:/Users/ASUS/Desktop/Thames' Work/Data Science Project 2024/Imputed Data"
)

# Initialize an empty list to collect data from each CSV file
csv_files = []

# Iterate through all the files in the folder
for filename in os.listdir(folder_path):
    # Check if the file is a CSV file
    if filename.endswith(".csv"):
        file_path = os.path.join(folder_path, filename)
        # Read the CSV file and append it to the list
        csv_files.append(pd.read_csv(file_path))

# Concatenate all dataframes in the list into a single dataframe
combined_df = pd.concat(csv_files, ignore_index=True)

# Save the combined dataframe to a new CSV file
combined_df.to_csv(
    "C:/Users/ASUS/Desktop/Thames' Work/Data Science Project 2024/New CSV/combined_output.csv",
    index=False,
)

print("CSV files have been combined successfully!")
