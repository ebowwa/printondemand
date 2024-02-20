# uuid_track/uuid_database.py

from .csv_database import CSVDatabase
from .uuid_generator import UUIDGenerator

class UUIDDatabase(CSVDatabase):
    def __init__(self, db_file: str):
        headers = ['UUID', 'File Name', 'Vision Prompt UUID', 'Chat Prompt UUID', 'Vision Response UUID', 'Chat Response UUID', 'Vision Response', 'Chat Response', 'Grade', 'Image Path/URL', 'Overlay Suggestion']
        super().__init__(db_file, headers)

    def add_entry(self, file_name: str, vision_response: str, chat_response: str, vision_prompt_uuid: str, chat_prompt_uuid: str, vision_response_uuid: str, chat_response_uuid: str, grade: str = None, image_path_url: str = '', overlay_suggestion=None):
        entry = {
            'UUID': UUIDGenerator.generate_uuid(),
            'File Name': file_name,
            'Vision Response': vision_response,
            'Chat Response': chat_response,
            'Vision Prompt UUID': vision_prompt_uuid,
            'Chat Prompt UUID': chat_prompt_uuid,
            'Vision Response UUID': vision_response_uuid,
            'Chat Response UUID': chat_response_uuid,
            'Grade': grade if grade is not None else '',
            'Image Path/URL': image_path_url,
            'Overlay Suggestion': overlay_suggestion or ""  # Use an empty string if no suggestion
        }
        super().add_entry(entry)

    def update_grade(self, uuid: str, grade: str):
        return self.update_entry(uuid, {'Grade': grade})
