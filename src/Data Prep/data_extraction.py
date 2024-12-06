import json
import os


def extract_details(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        try:
            data = json.load(file).get("abstracts-retrieval-response", {})
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in file: {file_path}") from e

    # Extracting details based on the provided structure
    extracted_data = {
        "Title": data.get("coredata", {}).get("dc:title", "Not Found"),
        "Authors": [],
        "Year": data.get("coredata", {}).get("prism:coverDate", "Not Found"),
        "Institution": [],
        "Location": [],
        "Keywords": "Not Available",
    }

    # Extracting authors
    authors = data.get("authors", {}).get("author", [])
    for author in authors:
        preferred_name = author.get("preferred-name", {})
        given_name = preferred_name.get("ce:given-name", "Unknown")
        surname = preferred_name.get("ce:surname", "Unknown")
        extracted_data["Authors"].append(f"{given_name} {surname}")

    # Extracting institution and location
    affiliations = data.get("affiliation", [])
    for affiliation in affiliations:
        institution = affiliation.get("affilname", "Unknown")
        city = affiliation.get("affiliation-city", "Unknown")
        country = affiliation.get("affiliation-country", "Unknown")
        extracted_data["Institution"].append(institution)
        extracted_data["Location"].append(f"{city}, {country}")

    # Clean duplicates and empty values
    extracted_data["Authors"] = list(set(filter(None, extracted_data["Authors"])))
    extracted_data["Institution"] = list(
        set(filter(None, extracted_data["Institution"]))
    )
    extracted_data["Location"] = list(set(filter(None, extracted_data["Location"])))

    return extracted_data


# Test JSON structure
file_path = (
    "src/Data Prep/Example Data/201800000.json"  # Replace with your JSON file path
)
try:
    details = extract_details(file_path)
    print("Extracted Details:")
    for key, value in details.items():
        print(f"{key}: {value}")
except (FileNotFoundError, ValueError) as e:
    print(f"Error: {e}")
