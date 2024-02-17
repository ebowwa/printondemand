from uuid import uuid4
import csv
import os

class UUIDDatabase:
    def __init__(self, db_file: str):
      self.db_file = db_file
      self.headers = ['UUID', 'File Name', 'Prompt', 'Response', 'Prompt UUID', 'Response UUID', 'Grade']
      self._initialize_db()
  
    def _initialize_db(self):
      """Initialize the database file with headers if it's new."""
      try:
          with open(self.db_file, 'x', newline='') as file:
              writer = csv.DictWriter(file, fieldnames=self.headers)
              writer.writeheader()
      except FileExistsError:
          # File already exists, no need to initialize
          pass

    def add_entry(self, file_name: str, prompt: str, response: str, prompt_uuid: str, response_uuid: str, grade: str = None):
        """Add a new entry to the database."""
        entry = {
            'UUID': str(uuid4()),
            'File Name': file_name,
            'Prompt': prompt,
            'Response': response,
            'Prompt UUID': prompt_uuid,
            'Response UUID': response_uuid,
            'Grade': grade if grade is not None else ''
        }
        with open(self.db_file, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            writer.writerow(entry)


    def search_entries(self, search_criteria: dict) -> list:
        """Search for entries matching the given criteria."""
        results = []
        with open(self.db_file, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if all(str(row.get(k, '')).lower() == str(v).lower() for k, v in search_criteria.items()):
                    results.append(row)
        return results

    def update_grade(self, uuid: str, grade: str):
        """Update the grade of an entry by its UUID."""
        updated = False
        temp_file = self.db_file + '.tmp'
        with open(self.db_file, 'r', newline='') as file, open(temp_file, 'w', newline='') as temp:
            reader = csv.DictReader(file)
            writer = csv.DictWriter(temp, fieldnames=self.headers)
            writer.writeheader()
            for row in reader:
                if row['UUID'] == uuid:
                    row['Grade'] = grade
                    updated = True
                writer.writerow(row)
        os.replace(temp_file, self.db_file)
        return updated
  
    def delete_entry(self, uuid: str):
        """Delete an entry by its UUID."""
        temp_file = self.db_file + '.tmp'
        with open(self.db_file, newline='') as file, open(temp_file, 'w', newline='') as tempfile:
            reader = csv.DictReader(file)
            writer = csv.DictWriter(tempfile, fieldnames=self.headers)
            writer.writeheader()
            for row in reader:
                if row['UUID'] != uuid:
                    writer.writerow(row)
        os.replace(temp_file, self.db_file)
