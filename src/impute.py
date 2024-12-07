import json
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the JSON file to extract data
file_path = "/Users/ppunpunppy/Desktop/٩(˘◡˘)۶/Data Science/Data Sci Hua Kuay/Cleaned_Data_NoCode/2018.json"
with open(file_path, 'r') as f:
    data = json.load(f)

# Extract relevant fields: Authors, Institution, Keywords, Classification Code
extracted_data = []
for entry in data:
    extracted_data.append({
        "Title": entry.get("Title", None),
        "Authors": entry.get("Authors", None),
        "Institution": entry.get("Institution", None),
        "Location": entry.get("Location", None),
        "Keywords": entry.get("Keywords", None),
        "Year": entry.get("Year", None),
    })

# Convert to a DataFrame for easier manipulation
df = pd.DataFrame(extracted_data)

print(df.columns)

# Step 1: Clean Institution Names
# Replace "not available" or similar placeholders in Institution with NaN
df['Institution'] = df['Institution'].apply(
    lambda x: [inst if inst.lower() != "not available" else np.nan for inst in x] if isinstance(x, list) else x
)
df['Institution'] = df['Institution'].apply(
    lambda x: [inst for inst in x if pd.notna(inst)] if isinstance(x, list) else x
)

# Create a mapping of authors to their known institutions
author_to_institution = {}

# Populate the author-to-institution mapping
for _, row in df.iterrows():
    if isinstance(row['Authors'], list) and isinstance(row['Institution'], list):
        for author in row['Authors']:
            if author not in author_to_institution:
                author_to_institution[author] = set()
            author_to_institution[author].update(row['Institution'])

# Step 2: Define the most common institution as a fallback
all_institutions = [inst for sublist in df['Institution'] for inst in sublist if isinstance(sublist, list)]
most_common_institution = pd.Series(all_institutions).mode()[0]

# Step 3: Impute missing institutions
def impute_institution(row):
    if not isinstance(row['Institution'], list) or len(row['Institution']) == 0:
        # Check co-authors' known institutions
        institutions = set()
        if isinstance(row['Authors'], list):
            for author in row['Authors']:
                if author in author_to_institution:
                    institutions.update(author_to_institution[author])
        if institutions:
            return list(institutions)
        # Fallback to most common institution
        return [most_common_institution]
    return row['Institution']

# Apply the function to impute missing institutions
df['Institution'] = df.apply(impute_institution, axis=1)

# Step 4: Update the author-to-institution mapping with imputed values
for _, row in df.iterrows():
    if isinstance(row['Authors'], list) and isinstance(row['Institution'], list):
        for author in row['Authors']:
            if author not in author_to_institution:
                author_to_institution[author] = set()
            author_to_institution[author].update(row['Institution'])




# Step 2: Impute Missing Keywords
# Use the paper title to infer keywords for missing ones
# Extract potential keywords using CountVectorizer for text similarity
vectorizer = CountVectorizer(stop_words='english', max_features=100)
title_vectors = vectorizer.fit_transform(df['Title'].fillna("No Title"))
title_terms = vectorizer.get_feature_names_out()

# Create a cosine similarity matrix for papers based on their titles
similarity_matrix = cosine_similarity(title_vectors)

# Define a function to infer keywords from similar papers
def infer_keywords(row_index):
    if len(df.loc[row_index, 'Keywords']) > 0:
        return df.loc[row_index, 'Keywords']
    # Find the most similar paper
    similar_indices = similarity_matrix[row_index].argsort()[::-1]
    for idx in similar_indices:
        if len(df.loc[idx, 'Keywords']) > 0:
            return df.loc[idx, 'Keywords']
    # Fallback to most common keywords in the dataset
    return [kw for kw in pd.Series([kw for sublist in df['Keywords'] for kw in sublist]).mode()]

# Replace 'Not Available' with NaN
df['Keywords'] = df['Keywords'].apply(lambda x: [kw if kw.lower() != "not available" else np.nan for kw in x] if isinstance(x, list) else x)
df['Keywords'] = df['Keywords'].apply(lambda x: [kw for kw in x if pd.notna(kw)] if isinstance(x, list) else x)

# Apply the inference function to each row for missing keywords
df['Keywords'] = df.apply(lambda row: infer_keywords(row.name), axis=1)

# Step 3: Normalize institution names and keywords
df['Institution'] = df['Institution'].apply(lambda x: [i.strip().lower() for i in x] if isinstance(x, list) else x)
df['Keywords'] = df['Keywords'].apply(lambda x: [kw.strip().lower() for kw in x] if isinstance(x, list) else x)

print(df['Keywords'].head())

print(df['Institution'].head())



# Step 3: Impute Missing Location
df['Location'] = df['Location'].apply(
    lambda x: [loc if loc.lower() != "not available" else np.nan for loc in x] if isinstance(x, list) else x
)
df['Location'] = df['Location'].apply(
    lambda x: [loc for loc in x if pd.notna(loc)] if isinstance(x, list) else x
)

# Step 1: Create a mapping of institutions to known locations
institution_to_location = {}

# Populate the mapping from existing data
for _, row in df.iterrows():
    if isinstance(row['Institution'], list) and isinstance(row['Location'], list):
        for inst, loc in zip(row['Institution'], row['Location']):
            if pd.notna(loc):  # Only map non-missing locations
                institution_to_location[inst] = loc

# Step 2: Define the fallback location
all_locations = [loc for sublist in df['Location'] for loc in sublist if isinstance(sublist, list)]
most_common_location = pd.Series(all_locations).mode()[0]

# Step 3: Impute missing locations
def impute_location(row):
    if not isinstance(row['Location'], list) or len(row['Location']) == 0:
        # Check if institutions can provide location information
        locations = set()
        if isinstance(row['Institution'], list):
            for inst in row['Institution']:
                if inst in institution_to_location:
                    locations.add(institution_to_location[inst])
        if locations:
            return list(locations)
        # Fallback to the most common location
        return [most_common_location]
    return row['Location']

# Apply the imputation function to the Location column
df['Location'] = df.apply(impute_location, axis=1)

print(df['Location'].head())

# Save the cleaned DataFrame to a CSV file
cleaned_file_path = '/Users/ppunpunppy/Desktop/٩(˘◡˘)۶/Data Science/Data Sci Hua Kuay/Cleaned_Data_CSV/2018.csv'
df.to_csv(cleaned_file_path, index=False)