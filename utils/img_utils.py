# utils/img_utils.py

from PIL import Image
import io, uuid, os

def open_image(image_path):
    """Open an image and return the PIL.Image object."""
    return Image.open(image_path)

def save_image(image, save_path, format='PNG', quality=100):
    """Save an image in the specified format and quality."""
    image.save(save_path, format=format, quality=quality)

def resize_image(image, target_width, target_height, resample=Image.Resampling.LANCZOS):
    """Resize an image to target dimensions, maintaining aspect ratio."""
    original_width, original_height = image.size
    aspect_ratio = original_width / original_height

    if target_width / aspect_ratio <= target_height:
        new_width = target_width
        new_height = int(target_width / aspect_ratio)
    else:
        new_width = int(target_height * aspect_ratio)
        new_height = target_height

    return image.resize((new_width, new_height), resample=resample)

def generate_unique_filename(extension='.png'):
    """Generate a unique filename with the specified extension."""
    return f"{uuid.uuid4()}{extension}"

def get_image_size_in_mb(image):
    """Calculate the image size in megabytes."""
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=image.format)
    size_mb = len(img_byte_arr.getvalue()) / (1024 * 1024)
    return size_mb

