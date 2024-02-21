#  utils/find_png.py
from .file_utils import list_files, join_paths

def find_uuid_png_files(directory, uuid):
    """Find and return a list of PNG files containing the specific UUID in their filenames."""
    uuid_png_files = []
    for filename in list_files(directory):
        if filename.endswith('.png') and uuid in filename:
            uuid_png_files.append(join_paths(directory, filename))
    return uuid_png_files
