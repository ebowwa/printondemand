# img_mod.py
# Modifies PNG files, expanding size to 4500x5400 and calculates the MB size of the image resized
# after png is sent to Gemini, due to size expansion
import os
from utils.resize import resize_image_proportionately
from utils.img_utils import get_image_size_in_mb
from utils.file_utils import create_directory, generate_path

def resize_and_save_image(image_path, target_width, target_height, save_dir):
    """
    Resize an image proportionately and save it to a specified directory.

    Parameters:
    image_path (str): Path to the input image.
    target_width (int): Target width for the resized image.
    target_height (int): Target height for the resized image.
    save_dir (str): Directory where the resized image will be saved.
    """
    # Ensure the save directory exists
    create_directory(save_dir)

    # Generate a save path for the resized image
    save_path = generate_path(save_dir, os.path.basename(image_path).replace('.png', '_resized.png'))

    # Resize the image proportionately
    resized_image = resize_image_proportionately(image_path, target_width, target_height, save_path)

    # Calculate the size of the resized image in MB
    size_mb = get_image_size_in_mb(resized_image)
    print(f"Resized image saved to {save_path}")
    print(f"Size of the resized image: {size_mb:.2f} MB")

if __name__ == "__main__":
  image_path = "response/cf52cb31-658e-4253-844b-df3ef2c86ba2.png"  # Update this to your image's path
  target_width = 4500
  target_height = 5400
  save_dir = "result"  # Update this to your desired save directory

  resize_and_save_image(image_path, target_width, target_height, save_dir)
