# utils/mb_size.py
from pydantic import BaseModel, Field, ValidationError
from typing import Any
from .img_utils import open_image, save_image, get_image_size_in_mb
import io

class ImageSize(BaseModel):
    image_path: str = Field(..., description="Path to the input image")
    max_size_mb: float = Field(..., gt=0, description="Maximum size of the image in megabytes")

    @classmethod
    def validate_max_size_mb(cls, value):
        if value <= 0:
            raise ValueError('Maximum size should be greater than 0.')
        return value

    def calculate_and_adjust_size(self):
        image = open_image(self.image_path)
        size_mb = get_image_size_in_mb(image)

        print(f"Initial image size: {size_mb:.2f} MB")

        while size_mb > self.max_size_mb:
            current_width, current_height = image.size
            image = image.resize((int(current_width * 0.9), int(current_height * 0.9)), Image.Resampling.LANCZOS)
            size_mb = get_image_size_in_mb(image)
            print(f"Adjusted image size: {size_mb:.2f} MB")

        # Optionally, save the adjusted image
        # save_image(image, 'path/to/save/adjusted_image.png')

        return image

if __name__ == "__main__":
    # Load a sample image
    sample_image = Image.open("response/d72e633a-1ba9-4495-a1b2-6c266a89e812.png")  # Update this path to your image file

    # Define the maximum size (in MB)
    max_size_mb = 25

    # Create an instance of ImageSize
    image_size = ImageSize(image=sample_image, max_size_mb=max_size_mb)

    # Adjust the image size
    modified_image = image_size.calculate_and_adjust_size()
    # Print the final size of the image (this will print the initial size if no adjustment was necessary)
    img_byte_arr = io.BytesIO()
    modified_image.save(img_byte_arr, format=modified_image.format)
    final_size_mb = len(img_byte_arr.getvalue()) / (1024 * 1024)
    print(f"Final image size: {final_size_mb:.2f} MB")
