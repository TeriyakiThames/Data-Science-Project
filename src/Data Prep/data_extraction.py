import json
import os


# Define a function to extract and clean data
def clean_data(json_file):
    try:
        with open(json_file, "r", encoding="utf-8") as file:
            try:
                data = json.load(file).get("abstracts-retrieval-response", {})
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON format in file: {json_file}") from e

        # Extracting details based on the provided structure
        extracted_data = {
            "Previous File": str(json_file),
            "Title": (
                data.get("coredata", {}).get("dc:title", "Not Available")
                if isinstance(data.get("coredata", {}), dict)
                else "Not Available"
            ),
            "Authors": [],
            "Date": (
                data.get("coredata", {}).get("prism:coverDate", "Not Available")
                if isinstance(data.get("coredata", {}), dict)
                else "Not Available"
            ),
            "Institution": [],
            "City": [],
            "Country": [],
            "Keywords": [],
            "Classification Code": [],
        }

        # Extracting authors
        authors = data.get("authors", {}).get("author", [])
        if authors:
            for author in authors:
                preferred_name = author.get("preferred-name", {})
                given_name = preferred_name.get("ce:given-name", "Unknown")
                surname = preferred_name.get("ce:surname", "Unknown")
                extracted_data["Authors"].append(f"{given_name} {surname}")
        else:
            extracted_data["Authors"] = ["Not Available"]

        affiliations = data.get("affiliation", [])
        if isinstance(affiliations, list):
            for affiliation in affiliations:
                if isinstance(affiliation, dict):
                    institution = affiliation.get("affilname", "Unknown")
                    city = affiliation.get("affiliation-city", "Unknown")
                    country = affiliation.get("affiliation-country", "Unknown")
                    extracted_data["Institution"].append(
                        institution if institution else "Not Available"
                    )
                    extracted_data["City"].append(
                        f"{city}" if city else "Not Available"
                    )
                    extracted_data["Country"].append(
                        f"{country}" if country else "Not Available"
                    )
        elif isinstance(affiliations, dict):
            institution = affiliations.get("affilname", "Unknown")
            city = affiliations.get("affiliation-city", "Unknown")
            country = affiliations.get("affiliation-country", "Unknown")
            extracted_data["Institution"].append(
                institution if institution else "Not Available"
            )
            extracted_data["City"].append(f"{city}" if city else "Not Available")
            extracted_data["Country"].append(
                f"{country}" if country else "Not Available"
            )
        else:
            extracted_data["Institution"] = ["Not Available"]
            extracted_data["City"] = ["Not Available"]
            extracted_data["Country"] = ["Not Available"]

        # Extracting keywords
        if data.get("authkeywords") != None:
            authkeywords = data.get("authkeywords", {}).get("author-keyword", [])
            if isinstance(authkeywords, list):
                for keyword in authkeywords:
                    if isinstance(keyword, dict):
                        k = keyword.get("$", "Not Available")
                        extracted_data["Keywords"].append(k if k else "Not Available")
        else:
            extracted_data["Keywords"] = ["Not Available"]

        # Extracting Classification Code
        subject_areas = data.get("subject-areas", {}).get("subject-area")
        if isinstance(subject_areas, list):
            for subject_area in subject_areas:
                code = subject_area.get("@code", "Unknown")
                extracted_data["Classification Code"].append(
                    code if code else "Unknown"
                )
        else:
            extracted_data["Classification Code"] = ["Unknown"]

        # Clean duplicates and empty values
        extracted_data["Authors"] = list(set(filter(None, extracted_data["Authors"])))
        extracted_data["Institution"] = list(
            set(filter(None, extracted_data["Institution"]))
        )
        extracted_data["City"] = list(set(filter(None, extracted_data["City"])))
        extracted_data["Country"] = list(set(filter(None, extracted_data["Country"])))

        return extracted_data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON file {json_file}: {e}")
        return None
    except AttributeError as e:
        print(f"Unexpected data structure in file {json_file}: {e}")
        return extracted_data
    except Exception as e:
        print(f"Unexpected error processing file {json_file}: {e}")
        return extracted_data


# Main function to process files and save results
def process_json_files(input_folder, output_folder):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    for year_folder in os.listdir(input_folder):
        year_path = os.path.join(input_folder, year_folder)
        if not os.path.isdir(year_path):
            continue  # Skip non-folder items

        cleaned_data = []

        for file_name in os.listdir(year_path):
            if file_name.endswith(".json"):
                json_file = os.path.join(year_path, file_name)
                cleaned_entry = clean_data(json_file)
                if cleaned_entry:
                    cleaned_data.append(cleaned_entry)

        # Save the cleaned data for the current year as a JSON file
        output_file = os.path.join(output_folder, f"{year_folder}.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(cleaned_data, f, indent=4, ensure_ascii=False)

        print(f"Saved cleaned data for {year_folder} to {output_file}")


# Specify input and output directories
input_folder = "C:/Users/ASUS/Desktop/Thames' Work/Data Science Project 2024/Project"
output_folder = (
    "C:/Users/ASUS/Desktop/Thames' Work/Data Science Project 2024/Cleaned Data"
)

# Run the processing function
process_json_files(input_folder, output_folder)
