# uuid_track/csv_database.py
import csv
import os

class CSVDatabase:
    def __init__(self, db_file: str, headers: list):
        self.db_file = db_file
        self.headers = headers
        self._initialize_db()

    def _initialize_db(self):
        try:
            with open(self.db_file, 'x', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=self.headers)
                writer.writeheader()
        except FileExistsError:
            pass

    def add_entry(self, entry: dict):
        with open(self.db_file, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            writer.writerow(entry)

    def search_entries(self, search_criteria: dict) -> list:
        results = []
        with open(self.db_file, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if all(str(row.get(k, '')).lower() == str(v).lower() for k, v in search_criteria.items()):
                    results.append(row)
        return results

    def update_entry(self, uuid: str, updates: dict):
        updated = False
        temp_file = self.db_file + '.tmp'
        with open(self.db_file, 'r', newline='') as file, open(temp_file, 'w', newline='') as temp:
            reader = csv.DictReader(file)
            writer = csv.DictWriter(temp, fieldnames=self.headers)
            writer.writeheader()
            for row in reader:
                if row['UUID'] == uuid:
                    row.update(updates)
                    updated = True
                writer.writerow(row)
        os.replace(temp_file, self.db_file)
        return updated

    def delete_entry(self, uuid: str):
        temp_file = self.db_file + '.tmp'
        with open(self.db_file, newline='') as file, open(temp_file, 'w', newline='') as tempfile:
            reader = csv.DictReader(file)
            writer = csv.DictWriter(tempfile, fieldnames=self.headers)
            writer.writeheader()
            for row in reader:
                if row['UUID'] != uuid:
                    writer.writerow(row)
        os.replace(temp_file, self.db_file)
