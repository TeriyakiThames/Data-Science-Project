import json
import os
import time


def combine_json_files(input_folder, output_file):
    combined_data = []

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):  # Process only JSON files
            file_path = os.path.join(input_folder, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # Add "Previous File" field with the file's relative path
                data["Previous File"] = file_path
                combined_data.append(data)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    # Write the combined data to the output file
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(combined_data, f, indent=4, ensure_ascii=False)
        print(f"Combined JSON file saved to {output_file}")
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")


# Set the folder containing JSON files and the output file path
input_folder = input("Enter the input folder:\n").strip('"')
output_folder = input("\nEnter the output folder:\n").strip('"')
output_file = os.path.join(output_folder, "combined.json")

start_time = time.time()

combine_json_files(input_folder, output_file)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"\nTime taken: {elapsed_time:.2f} seconds")
