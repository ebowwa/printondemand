# add function to return png file location aswell 
import pandas as pd

class FlexibleCSVDatabase:
    def __init__(self, db_file: str):
        self.db_file = db_file

    def search_entries(self, search_criteria: dict) -> pd.DataFrame:
        data = pd.read_csv(self.db_file)
        for key, value in search_criteria.items():
            data = data[data[key].astype(str).str.contains(value, case=False, na=False)]
        return data

def get_row_info_by_filename(db, file_name):
    """Retrieve all information for a specific row based on the file name."""
    search_criteria = {'File Name': file_name}
    result = db.search_entries(search_criteria)
    return result

def get_prompt_info_by_uuid(prompt_db, uuids):
    """Given UUIDs, find and retrieve prompt details from the prompt database."""
    results = []
    for uuid in uuids:
        result = prompt_db.search_entries({'Prompt UUID': uuid})
        results.append(result)
    return pd.concat(results) if results else pd.DataFrame()

if __name__ == "__main__":
    # Example usage
    uuid_db_path = 'data_2024-02-20_23-48-53/uuid_data.csv'  # Adjust path accordingly
    prompt_db_path = 'data_2024-02-20_23-48-53/prompt_data.csv'  # Adjust path accordingly

    uuid_db = FlexibleCSVDatabase(uuid_db_path)
    prompt_db = FlexibleCSVDatabase(prompt_db_path)

    # Search for a specific file's information
    file_name = 'response/00c90244-64ea-49fa-b26b-63394a92a088.png'
    row_info = get_row_info_by_filename(uuid_db, file_name)
    print("Row Information:", row_info)

    # Assuming row_info contains 'Vision Prompt UUID' and 'Chat Prompt UUID', extract them
    if not row_info.empty:
        vision_prompt_uuid = row_info.iloc[0]['Vision Prompt UUID']
        chat_prompt_uuid = row_info.iloc[0]['Chat Prompt UUID']

        # Retrieve prompt information using UUIDs
        prompt_uuids = [vision_prompt_uuid, chat_prompt_uuid]
        prompt_info = get_prompt_info_by_uuid(prompt_db, prompt_uuids)
        print("Prompt Information:", prompt_info)
