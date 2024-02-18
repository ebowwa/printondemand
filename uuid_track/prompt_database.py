# uuid_track/prompt_database.py

import csv
import os
from uuid import uuid4

class PromptDatabase:
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.headers = ['Prompt UUID', 'Prompt']
        self._initialize_db()

    def _initialize_db(self):
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=self.headers)
                writer.writeheader()

    def find_prompt_uuid(self, prompt: str):
        with open(self.db_file, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Prompt'] == prompt:
                    return row['Prompt UUID']
        return None

    def add_entry(self, prompt: str):
        existing_uuid = self.find_prompt_uuid(prompt)
        if existing_uuid is None:
            prompt_uuid = str(uuid4())
            entry = {'Prompt UUID': prompt_uuid, 'Prompt': prompt}
            with open(self.db_file, 'a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=self.headers)
                writer.writerow(entry)
        else:
            prompt_uuid = existing_uuid
        return prompt_uuid
