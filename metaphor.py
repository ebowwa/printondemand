import pandas as pd
import glob
import os

class FlexibleCSVDatabase:
    def __init__(self, db_file: str):
        self.db_file = db_file

    def search_entries(self, search_criteria: dict) -> pd.DataFrame:
        data = pd.read_csv(self.db_file)
        for key, value in search_criteria.items():
            data = data[data[key].astype(str).str.contains(value, case=False, na=False)]
        return data

def find_uuid_png_files(directory, uuid):
    uuid_png_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.png') and uuid in filename:
                uuid_png_files.append(os.path.join(root, filename))
    return uuid_png_files

def execute_search(uuid_db_path, prompt_db_path, directory, file_name):
    uuid_db = FlexibleCSVDatabase(uuid_db_path)
    prompt_db = FlexibleCSVDatabase(prompt_db_path)

    row_info = uuid_db.search_entries({'File Name': file_name})
    if not row_info.empty:
        print("Row Information:\n", row_info.to_string(index=False, header=True))

        # Extract the UUID from the file_name for PNG search
        file_uuid = file_name.split('.')[0]  # Assuming UUID is the filename without the extension

        # Find PNG files associated with the UUID extracted from file_name
        png_files = find_uuid_png_files(directory, file_uuid)
        print("\nPNG Files:", png_files if png_files else "No PNG files found.")
    else:
        print("No row information found for the given file name.")

if __name__ == "__main__":
    # Adjust these paths and variables according to your setup
    uuid_db_path = 'data_2024-02-20_23-48-53/uuid_data.csv'
    prompt_db_path = 'data_2024-02-20_23-48-53/prompt_data.csv'
    directory = 'response'
    file_name = '00c90244-64ea-49fa-b26b-63394a92a088.png'

    execute_search(uuid_db_path, prompt_db_path, directory, file_name)
