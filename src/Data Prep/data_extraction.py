import json
import os
import time


class Extract_data:
    def __init__(self):
        self.data = None

    # Opens and reads the contents of the json file
    def open_file(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as file:
            try:
                self.data = json.load(file).get("abstracts-retrieval-response", {})
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON format in file: {file_path}") from e

    # Extract data such as title, authors, year, institution, and location
    def extract_details(self, file_path):
        self.open_file(file_path)

        extracted_data = {
            "Title": self.data.get("coredata", {}).get("dc:title", "Not Found"),
            "Authors": [],
            "Year": self.data.get("coredata", {}).get("prism:coverDate", "Not Found"),
            "Institution": [],
            "Location": [],
        }

        # Extracting authors
        authors = self.data.get("authors", {}).get("author", [])
        for author in authors:
            preferred_name = author.get("preferred-name", {})
            given_name = preferred_name.get("ce:given-name", "Unknown")
            surname = preferred_name.get("ce:surname", "Unknown")
            extracted_data["Authors"].append(f"{given_name} {surname}")

        # Extracting institution and location
        affiliations = self.data.get("affiliation", [])
        if isinstance(affiliations, dict):  # if it's a single dictionary
            affiliations = [affiliations]  # make it a list for uniform processing

        for affiliation in affiliations:
            # Ensure affiliation is a dictionary before accessing its fields
            if isinstance(affiliation, dict):
                institution = affiliation.get("affilname", "Unknown")
                city = affiliation.get("affiliation-city", "Unknown")
                country = affiliation.get("affiliation-country", "Unknown")
            else:
                # If it's a string, handle it differently (e.g., set some default values)
                institution = "Unknown"
                city = "Unknown"
                country = "Unknown"

            extracted_data["Institution"].append(institution)
            extracted_data["Location"].append(f"{city}, {country}")

        # Clean duplicates and empty values
        extracted_data["Authors"] = list(set(filter(None, extracted_data["Authors"])))
        extracted_data["Institution"] = list(
            set(filter(None, extracted_data["Institution"]))
        )
        extracted_data["Location"] = list(set(filter(None, extracted_data["Location"])))
        self.extracted_data = extracted_data
        return extracted_data


start_time = time.time()

for i in range(0, 2791):
    # Enter your file path here:
    file_path = f"C:/Users/ASUS/Desktop/Thames' Work/Data Science Project 2024/Project/2018/2018{str(i).zfill(5)}.json"
    ED_class = Extract_data()

    try:
        details = ED_class.extract_details(file_path=file_path)

        # Print the extracted details
        print(
            f"\nExtracted Details of 2018{str(i).zfill(5)}: =================================================="
        )
        for key, value in details.items():
            print(f"{key}: {value}")

    except (FileNotFoundError, ValueError) as e:
        print(f"Error processing file 2018{str(i).zfill(5)}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

end_time = time.time()
elapsed_time = end_time - start_time
# Print the time taken to process the file
print(f"Time taken: {elapsed_time:.2f} seconds")
