import argparse
import zipfile
import os
import shutil
import fnmatch

def parse_arguments():
    parser = argparse.ArgumentParser(description='Unzip a zip file containing .webp images and clean up unwanted files.')
    parser.add_argument('--file_path', type=str, help='Path to the zip file to be unzipped.')
    return parser.parse_args()

def delete_unwanted_files(root_dir, patterns):
    for root, dirs, files in os.walk(root_dir, topdown=False):
        for pattern in patterns:
            for dir in fnmatch.filter(dirs, pattern):
                shutil.rmtree(os.path.join(root, dir))
                print(f"Deleted directory: {os.path.join(root, dir)}")
            for file in fnmatch.filter(files, pattern):
                os.remove(os.path.join(root, file))
                print(f"Deleted file: {os.path.join(root, file)}")

def unzip_file(zip_path, extract_to='unzipped_content'):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extracted all contents to {extract_to}")

    # Read .unzipignore file and delete specified patterns
    ignore_file = os.path.join(extract_to, '.unzipignore')
    patterns = ['__MACOSX', '.DS_Store']  # Default patterns to ignore
    if os.path.exists(ignore_file):
        with open(ignore_file, 'r') as f:
            patterns.extend(line.strip() for line in f.readlines())
    delete_unwanted_files(extract_to, patterns)

def main():
    args = parse_arguments()
    zip_path = args.file_path

    # Unzip the file
    unzip_file(zip_path)

    # Placeholder for further processing of .webp images
    print("Placeholder for further .webp image processing.")

if __name__ == "__main__":
    main()



# python utils/unzip_script.py --file_path your_zip_file.zip
# i.e. python utils/cli-unzip.py --file_path discord_Midjorneyv6.zip