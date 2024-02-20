# utils/find_png.py

from .file_utils import list_files, join_paths, create_directory

def find_list_uuid_png_files(directory):
    """Find and return a list of PNG files containing UUIDs in their filenames."""
    uuid_list_png_files = []
    for filename in list_files(directory):
        if filename.endswith('.png') and '-' in filename:
          uuid_list_png_files.append(join_paths(directory, filename))
    return uuid_list_png_files

if __name__ == "__main__":
    directory = input("Enter the directory path: ")
    uuid_list_png_files = find_list_uuid_png_files(directory)
    print("Found UUID PNG files:")
    for file in uuid_list_png_files:
        print(file)
