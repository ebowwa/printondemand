# utils/resize.py, refactored version

from .img_utils import open_image, save_image, resize_image

def resize_image_proportionately(image_path, target_width, target_height, save_path=None):
    img = open_image(image_path)
    resized_img = resize_image(img, target_width, target_height)
    if save_path:
        save_image(resized_img, save_path)
    return resized_img

# Example usage
# image_path = "response/af3a5acd-e70e-4b03-8563-15c8b62d27fa.png"
# target_width = 4500
# target_height = 5400
# save_path = "resized_image.jpg"

# resized_image = resize_image_proportionately(image_path, target_width, target_height, save_path)
# print(f"Resized image saved to {save_path}")

# If you don't want to save the image immediately, you can remove the save_path argument
# and work with the 'resized_image' object directly in your Python script.
