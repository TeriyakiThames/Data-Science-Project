import os
import time


# Change extensions of the data files to json
def change_extension(directory):
    # Traverse all subdirectories and files
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)

            # Check if the file has no extension
            if os.path.isfile(filepath) and not os.path.splitext(filename)[1]:
                new_filename = filename + ".json"
                new_filepath = os.path.join(root, new_filename)
                os.rename(filepath, new_filepath)
                print(f"Renamed: {filepath} -> {new_filepath}")


# Start timing
start_time = time.perf_counter()

# Get user input and execute the function
root_directory = input("Enter root directory here: ").strip('"')
change_extension(root_directory)

# End timing
end_time = time.perf_counter()

elapsed_time = end_time - start_time
print(f"Renaming complete! Time taken: {elapsed_time:.2f} seconds")
