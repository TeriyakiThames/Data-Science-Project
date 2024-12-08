import os


class ChangeExtension:
    # Change extensions of the data files to json
    def change_extension(self, directory):
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
