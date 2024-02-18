# Adjusted WebpToPngConverter class with UUID integration for unique naming
from PIL import Image
import os
import uuid

class WebpToPngConverter:
    def __init__(self, source_directory, target_directory):
        '''
        Initializes the converter with source and target directories.
        '''
        self.source_directory = source_directory
        self.target_directory = target_directory
        os.makedirs(self.target_directory, exist_ok=True)

    def convert_webp_to_png(self, source_path, target_path):
        '''
        Converts a WEBP image to PNG format.
        '''
        with Image.open(source_path) as img:
            img.save(target_path, 'PNG')

    def convert_all(self):
        conversion_details = []
        for webp_file in os.listdir(self.source_directory):
            if webp_file.endswith('.webp'):
                unique_id = uuid.uuid4()
                target_file_name = f"{unique_id}.png"
                target_file_path = os.path.join(self.target_directory, target_file_name)
                source_file_path = os.path.join(self.source_directory, webp_file)
                self.convert_webp_to_png(source_file_path, target_file_path)
                conversion_details.append({
                    'original_filename': webp_file,
                    'uuid_filename': target_file_name,
                    'file_path': target_file_path
                })
                print(f'Converted {webp_file} to PNG format with UUID {unique_id}.')
        return conversion_details


if __name__ == "__main__":
  source_directory = "unzipped_content/discord_Midjorneyv6"
  target_directory = "response"
  converter = WebpToPngConverter(source_directory, target_directory)
  conversion_details = converter.convert_all()
