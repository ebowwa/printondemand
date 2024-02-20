# search_interface.py

import csv
from uuid_track.uuid_database import UUIDDatabase
from uuid_track.prompt_database import PromptDatabase
from utils.find_png import find_uuid_png_files

class SearchInterface:
    def __init__(self, uuid_db_path: str, prompt_db_path: str, png_directory: str):
        self.uuid_database = UUIDDatabase(uuid_db_path)
        self.prompt_database = PromptDatabase(prompt_db_path)
        self.png_directory = png_directory

    def search_by_uuid(self, uuid: str) -> dict:
        """
        Enhanced search function to retrieve all information associated with a UUID.
        Includes prompts, responses, and PNG file paths.
        """
        # Search in UUID database
        uuid_records = self.uuid_database.search_entries({'UUID': uuid})
        prompt_uuids = [record['Prompt UUID'] for record in uuid_records]
        response_uuids = [record['Response UUID'] for record in uuid_records]

        # Search in Prompt database using prompt_uuids and response_uuids
        prompts = [self.prompt_database.search_entries({'Prompt UUID': pu}) for pu in prompt_uuids]
        responses = [self.prompt_database.search_entries({'Response UUID': ru}) for ru in response_uuids]

        # Find PNG files associated with the UUID
        png_files = find_uuid_png_files(self.png_directory, uuid)

        return {
            'uuid_records': uuid_records,
            'prompts': prompts,
            'responses': responses,
            'png_files': png_files
        }

# only returns the search uuid - although returns what type of content(prompt, img, response)
# Do the model responses get uuid's currently?
# should return all relevant content to uuid, i.e. if image uuid - return prompt uuid's, reponse uuid's, 
# error Cannot access member "search_entries" for type "PromptDatabase" Member "search_entries" is unknown