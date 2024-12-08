import glob
import json
import os

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ImputeMissingValue:
    def load_json(self, file_path):
        """Load the JSON file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading file {file_path}: {e}")
            return None

    def extract_data(self, data):
        """Extract relevant fields from the raw JSON data."""
        extracted_data = []
        for entry in data:
            extracted_data.append(
                {
                    "Title": entry.get("Title", None),
                    "Authors": entry.get("Authors", None),
                    "Institution": entry.get("Institution", None),
                    "City": entry.get("City", None),
                    "Country": entry.get("Country", None),
                    "Keywords": entry.get("Keywords", None),
                    "Date": entry.get("Date", None),
                }
            )
        return pd.DataFrame(extracted_data)

    def clean_institution_names(self, df):
        """Clean institution names, remove 'not available' and NaNs."""
        df["Institution"] = df["Institution"].apply(
            lambda x: (
                [inst for inst in x if inst.lower() != "not available"]
                if isinstance(x, list)
                else x
            )
        )
        df["Institution"] = df["Institution"].apply(
            lambda x: (
                [inst for inst in x if pd.notna(inst)] if isinstance(x, list) else x
            )
        )
        return df

    def create_author_to_institution_mapping(self, df):
        """Create a mapping of authors to their known institutions."""
        author_to_institution = {}
        for _, row in df.iterrows():
            if isinstance(row["Authors"], list) and isinstance(
                row["Institution"], list
            ):
                for author in row["Authors"]:
                    author_to_institution.setdefault(author, set()).update(
                        row["Institution"]
                    )
        return author_to_institution

    def impute_institution(self, row, author_to_institution, most_common_institution):
        """Impute missing institutions for authors."""
        if not isinstance(row["Institution"], list) or len(row["Institution"]) == 0:
            institutions = set()
            if isinstance(row["Authors"], list):
                for author in row["Authors"]:
                    if author in author_to_institution:
                        institutions.update(author_to_institution[author])
            if institutions:
                return list(institutions)
            return [most_common_institution]
        return row["Institution"]

    def clean_keywords(self, df):
        """Clean and impute missing keywords."""
        vectorizer = CountVectorizer(stop_words="english", max_features=100)
        title_vectors = vectorizer.fit_transform(df["Title"].fillna("No Title"))
        similarity_matrix = cosine_similarity(title_vectors)

        df["Keywords"] = df["Keywords"].apply(
            lambda x: [kw for kw in x if pd.notna(kw)] if isinstance(x, list) else x
        )
        df["Keywords"] = df.apply(
            lambda row: self.infer_keywords(row, df, similarity_matrix), axis=1
        )

        return df

    def infer_keywords(self, row, df, similarity_matrix):
        """Infer missing keywords based on the cosine similarity of titles."""
        keywords = row["Keywords"]

        # Check if the 'Keywords' column is not empty
        if keywords and len(keywords) > 0:
            return keywords

        # If no keywords are available for the current row, find the most similar rows
        similar_indices = similarity_matrix[row.name].argsort()[
            ::-1
        ]  # row.name gives the index
        for idx in similar_indices:
            similar_keywords = df.loc[idx, "Keywords"]
            if similar_keywords and len(similar_keywords) > 0:
                return similar_keywords

        # If no similar rows with keywords, infer based on the most common keywords
        all_keywords = [
            kw
            for sublist in df["Keywords"]
            if isinstance(sublist, list)
            for kw in sublist
        ]
        return (
            pd.Series(all_keywords).mode().tolist()
        )  # Return the most common keywords

    def clean_location(self, df, column_name):
        """Clean city and country columns."""
        df[column_name] = df[column_name].apply(
            lambda x: (
                [item if item.lower() != "not available" else np.nan for item in x]
                if isinstance(x, list)
                else x
            )
        )
        df[column_name] = df[column_name].apply(
            lambda x: (
                [item for item in x if pd.notna(item)] if isinstance(x, list) else x
            )
        )
        return df

    def save_to_csv(self, df, file_path):
        """Save the cleaned DataFrame to a CSV file."""
        df.to_csv(file_path, index=False)

    def impute_missing_dates(self, df):
        """Impute missing dates with the most common date."""
        most_common_date = (
            df["Date"].mode()[0] if not df["Date"].isnull().all() else None
        )
        df["Date"] = df["Date"].fillna(most_common_date)
        return df

    def run(self, folder_path, output_folder):
        """Main method to process and clean all JSON files in a directory."""
        if not os.path.isdir(folder_path):
            print(f"The folder '{folder_path}' does not exist.")
            return

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        json_files = glob.glob(os.path.join(folder_path, "*.json"))

        if not json_files:
            print(f"No .json files found in the folder '{folder_path}'.")
            return

        for file_path in json_files:
            print(f"Processing file: {file_path}")

            data = self.load_json(file_path)
            if data is None:
                continue

            df = self.extract_data(data)

            # Clean institution names and create author-to-institution mapping
            df = self.clean_institution_names(df)
            author_to_institution = self.create_author_to_institution_mapping(df)

            all_institutions = [
                inst
                for sublist in df["Institution"]
                for inst in sublist
                if isinstance(sublist, list)
            ]
            most_common_institution = (
                pd.Series(all_institutions).mode()[0] if all_institutions else "Unknown"
            )

            df = self.impute_missing_dates(df)

            # Impute missing institutions
            df["Institution"] = df.apply(
                lambda row: self.impute_institution(
                    row, author_to_institution, most_common_institution
                ),
                axis=1,
            )

            # Clean and impute missing keywords
            df = self.clean_keywords(df)

            # Clean city and country columns
            df = self.clean_location(df, "City")
            df = self.clean_location(df, "Country")

            output_file_name = (
                os.path.splitext(os.path.basename(file_path))[0] + "_cleaned.csv"
            )
            output_file_path = os.path.join(output_folder, output_file_name)

            self.save_to_csv(df, output_file_path)
            print(f"Cleaned data is saved\n")

        print(f"All files processed and saved in: {output_folder}")
