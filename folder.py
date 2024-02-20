# folder.py
import os
from img_mod import resize_and_save_image  # Import the resizing function from img_mod.py
from single_img import process_image_and_chat, initialize_directories, initialize_databases, load_generation_config, load_chat_config, read_prompt_from_markdown_with_validation

def process_images_in_folder(folder_path, vision_markdown_file_path, chat_markdown_file_path):
    dir_name = initialize_directories()
    db, prompt_db = initialize_databases(dir_name)
    generation_config = load_generation_config()
    model_name, chat_generation_config = load_chat_config()
    vision_prompt = read_prompt_from_markdown_with_validation(vision_markdown_file_path)
    chat_prompt = read_prompt_from_markdown_with_validation(chat_markdown_file_path)
    save_dir = "result"  # Specify the directory where resized images will be saved

    for image_file in os.listdir(folder_path):
        if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, image_file)
            # Process the image and chat based on the prompts
            process_image_and_chat(image_path, vision_prompt, chat_prompt, generation_config, chat_generation_config, dir_name, db, prompt_db, model_name)
            # After processing and before sending to Gemini, resize the image
            if image_file.lower().endswith('.png'):  # Check if the image is a PNG before resizing
                resize_and_save_image(image_path, 4500, 5400, save_dir)

if __name__ == "__main__":
    folder_path = 'response'
    vision_markdown_file_path = '_prompts/product/extract_product_details.md'
    chat_markdown_file_path = '_prompts/chat/v1.md'
    process_images_in_folder(folder_path, vision_markdown_file_path, chat_markdown_file_path)
