# uuid_track/uuid_database.py

from .csv_database import CSVDatabase
from .uuid_generator import UUIDGenerator

class UUIDDatabase(CSVDatabase):
    def __init__(self, db_file: str):
        headers = ['UUID', 'File Name', 'Prompt', 'Response', 'Prompt UUID', 'Response UUID', 'Grade', 'Image Path/URL', 'overlay_suggestion']
        super().__init__(db_file, headers)

    def add_entry(self, file_name: str, response: str, prompt_uuid: str, response_uuid: str, grade: str = None, image_path_url: str = '', prompt: str = None, overlay_suggestion=None):
        entry = {
            'UUID': UUIDGenerator.generate_uuid(),
            'File Name': file_name,
            'Response': response,
            'Prompt UUID': prompt_uuid,
            'Response UUID': response_uuid,
            'Grade': grade if grade is not None else '',
            'Image Path/URL': image_path_url,
            'overlay_suggestion': overlay_suggestion or ""  # Use an empty string if no suggestion
        }
        if prompt is not None:
            entry['Prompt'] = prompt  # Add prompt to the entry only if it is provided

        super().add_entry(entry)

    def update_grade(self, uuid: str, grade: str):
        return self.update_entry(uuid, {'Grade': grade})
