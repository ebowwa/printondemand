
from PIL import Image
import os

def convert_webp_to_png(source_path, target_path):
    '''
    Converts a WEBP image to PNG format.

    Parameters:
    - source_path: The path to the source WEBP image.
    - target_path: The path to save the converted PNG image.
    '''
    with Image.open(source_path) as img:
        img.save(target_path, 'PNG')

def main():
    source_directory = 'unzipped_content/discord_Midjorneyv6'  # Directory where the .webp images are located
    target_directory = 'png_images'  # Directory to save the .png images
    os.makedirs(target_directory, exist_ok=True)

    for webp_file in os.listdir(source_directory):
        if webp_file.endswith('.webp'):
            source_file_path = os.path.join(source_directory, webp_file)
            target_file_path = os.path.join(target_directory, webp_file.rsplit('.', 1)[0] + '.png')
            convert_webp_to_png(source_file_path, target_file_path)
            print(f'Converted {webp_file} to PNG format.')

if __name__ == '__main__':
    main()
