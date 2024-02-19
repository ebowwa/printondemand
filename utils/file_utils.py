# utils/file_utils.py
# os wrapper
import os
from pathlib import Path

def create_directory(directory_path):
    """Create a directory if it does not already exist."""
    os.makedirs(directory_path, exist_ok=True)

def list_files(directory_path, extension=None):
    """List all files in a directory, optionally filtering by extension."""
    files = os.listdir(directory_path)
    if extension:
        return [file for file in files if file.endswith(extension)]
    return files

def join_paths(*paths):
    """Join multiple paths into a single path."""
    return os.path.join(*paths)

def file_exists(file_path):
    """Check if a file exists."""
    return os.path.exists(file_path)

def directory_exists(directory_path):
    """Check if a directory exists."""
    return os.path.isdir(directory_path)

def generate_path(directory, filename):
    """Generate a file path by combining directory and filename."""
    return Path(directory) / filename
