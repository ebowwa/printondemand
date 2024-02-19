# utils/initializer.py

from datetime import datetime
from uuid_track.uuid_database import UUIDDatabase
from uuid_track.prompt_database import PromptDatabase
from .file_utils import create_directory  # Importing create_directory function

def initialize_directories():
    run_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dir_name = f"data_{run_time}"
    create_directory(dir_name)  # Using create_directory from file_utils
    return dir_name

def initialize_databases(dir_name):
    db = UUIDDatabase(f'{dir_name}/uuid_data.csv')
    prompt_db = PromptDatabase(f'{dir_name}/prompt_data.csv')
    return db, prompt_db
