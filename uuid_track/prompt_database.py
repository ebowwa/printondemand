# uuid_track/prompt_database.py
import csv
import os
from uuid import uuid4

class PromptDatabase:
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.headers = ['Prompt UUID', 'Prompt', 'Prompt Role']  # Added 'Prompt Role'
        self._initialize_db()

    def _initialize_db(self):
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=self.headers)
                writer.writeheader()

    def search_entries(self, search_criteria: dict) -> list:
        results = []
        with open(self.db_file, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if all(str(row.get(k, '')).lower() == str(v).lower() for k, v in search_criteria.items()):
                    results.append(row)
        return results


    def find_prompt_uuid(self, prompt: str, prompt_role: str):  # Added prompt_role parameter
        with open(self.db_file, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Prompt'] == prompt and row['Prompt Role'] == prompt_role:
                    return row['Prompt UUID']
        return None

    def add_entry(self, prompt: str, prompt_role: str):  # Added prompt_role parameter
        existing_uuid = self.find_prompt_uuid(prompt, prompt_role)
        if existing_uuid is None:
            prompt_uuid = str(uuid4())
            entry = {'Prompt UUID': prompt_uuid, 'Prompt': prompt, 'Prompt Role': prompt_role}  # Include prompt_role in entry
            with open(self.db_file, 'a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=self.headers)
                writer.writerow(entry)
        else:
            prompt_uuid = existing_uuid
        return prompt_uuid
