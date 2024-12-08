import time

from change_extension import ChangeExtension
from data_extraction import DataExtracter
from impute_missing_value import ImputeMissingValue


def change_the_extensions(root_directory):
    ce = ChangeExtension()
    ce.change_extension(root_directory)


def extract_data(input_folder, output_folder):
    change_the_extensions(input_folder)
    processor = DataExtracter(input_folder, output_folder)
    processor.process_json_files()


def impute_values(folder_path, output_folder):
    imputer = ImputeMissingValue()
    imputer.run(folder_path, output_folder)


def run():
    # Set up folders for extracting and imputing
    # starting_folder = input("Enter input folder path:\n").strip('"')
    # starting_folder = starting_folder.replace("\\", "/")

    extracted_folder = input("\nEnter folder path to extract files to:\n").strip('"')
    extracted_folder = extracted_folder.replace("\\", "/")

    imputed_folder = input(
        "\nEnter folder path to save the cleaned CSV files:\n"
    ).strip('"')
    imputed_folder = imputed_folder.replace("\\", "/")

    # Run the classes
    # extract_data(starting_folder, extracted_folder)
    impute_values(extracted_folder, imputed_folder)


start_time = time.time()

run()

end_time = time.time()
elapsed_time = end_time - start_time
print(f"\nTime taken: {elapsed_time:.2f} seconds")
