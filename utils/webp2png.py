# utils/webp2png.py
# utils/webp2png.py, refactored version

from img_utils import open_image, save_image, generate_unique_filename
import os

class WebpToPngConverter:
    def __init__(self, source_directory, target_directory):
        self.source_directory = source_directory
        self.target_directory = target_directory
        os.makedirs(self.target_directory, exist_ok=True)

    def convert_webp_to_png(self, source_path, target_path=None):
        if not target_path:
            target_path = os.path.join(self.target_directory, generate_unique_filename('.png'))
        img = open_image(source_path)
        save_image(img, target_path, 'PNG')
        return target_path

    def convert_all(self):
        conversion_details = []
        for webp_file in os.listdir(self.source_directory):
            if webp_file.endswith('.webp'):
                source_file_path = os.path.join(self.source_directory, webp_file)
                target_file_path = self.convert_webp_to_png(source_file_path)
                conversion_details.append({
                    'original_filename': webp_file,
                    'converted_filename': os.path.basename(target_file_path),
                    'file_path': target_file_path
                })
                print(f"Converted {webp_file} to PNG format.")
        return conversion_details


if __name__ == "__main__":
  source_directory = "unzipped_content/discord_Midjorneyv6"
  target_directory = "response"
  converter = WebpToPngConverter(source_directory, target_directory)
  conversion_details = converter.convert_all()
