# main.py
import os
import json
from datetime import datetime
import logging
from vision import generate_content_from_image
from uuid import uuid4
from uuid_track.uuid_database import UUIDDatabase
from uuid_track.prompt_database import PromptDatabase

def read_prompt_from_markdown(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

def load_generation_config(config_path):
    with open(config_path, 'r') as file:
        return json.load(file)["generation_config"]

def process_images_in_folder(folder_path, markdown_file_path, generation_config):
    run_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dir_name = f"data_{run_time}"
    os.makedirs(dir_name, exist_ok=True)

    db = UUIDDatabase(f'{dir_name}/uuid_data.csv')
    prompt_db = PromptDatabase(f'{dir_name}/prompt_data.csv')

    prompt = read_prompt_from_markdown(markdown_file_path)

    for image_filename in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_filename)
        if os.path.isfile(image_path):
            try:
                prompt_uuid = str(uuid4())
                prompt_uuid = prompt_db.add_entry(prompt=prompt)

                response_text = generate_content_from_image(image_path, prompt, generation_config)

                if response_text == "Failed to receive a valid response after multiple attempts.":
                    logging.error(f"Failed to generate content for {image_path}")
                    continue

                response_uuid = str(uuid4())
                db.add_entry(file_name=image_filename, response=response_text,
                             prompt_uuid=prompt_uuid, response_uuid=response_uuid, image_path_url=image_path)

                logging.info(f"Processed {image_path} successfully.")
            except Exception as e:
                logging.error(f"Error processing {image_path}: {e}")

# review newly created csv have embeddings review product details for each image
# add a GPT to suggest words to add as an overlay on to the image

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="process_log.txt", filemode="a",
                        format="%(asctime)s - %(levelname)s - %(message)s")
    image_folder_path = 'response'  # Folder containing images
    markdown_file_path = '_prompts/extract_product_details.md'
    generation_config_path = 'gemini/vision_config.json'  # Path to the generation configuration

    generation_config = load_generation_config(generation_config_path)

    process_images_in_folder(image_folder_path, markdown_file_path, generation_config)
