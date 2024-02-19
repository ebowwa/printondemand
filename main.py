# Updated main.py to include chat session and read prompt with validation
import os
import json
from datetime import datetime
import logging
from vision import generate_content_from_image  # Ensure this is your vision model's import path
from uuid import uuid4
from uuid_track.uuid_database import UUIDDatabase
from uuid_track.prompt_database import PromptDatabase
from gemini.chat_session import ChatSession  # Ensure this is your chat model's import path
from utils.read_prompt import read_prompt_from_markdown, ReadPromptRequest  # Adjusted import

def read_prompt_from_markdown_with_validation(file_path):
    request = ReadPromptRequest(file_path=file_path)
    return read_prompt_from_markdown(request)

def load_generation_config(config_path='gemini/vision_config.json'):
    with open(config_path, 'r') as file:
        return json.load(file)["generation_config"]

def load_chat_config(config_path='gemini/pro_config.json'):
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    model_name = config.get("generation_config", {}).pop("gen_model_name", None)
    chat_generation_config = config.get("generation_config", {})
    return model_name, chat_generation_config

def process_images_in_folder(folder_path, vision_markdown_file_path, chat_markdown_file_path, generation_config, chat_generation_config, model_name):
    run_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dir_name = f"data_{run_time}"
    os.makedirs(dir_name, exist_ok=True)

    db = UUIDDatabase(f'{dir_name}/uuid_data.csv')
    prompt_db = PromptDatabase(f'{dir_name}/prompt_data.csv')

    vision_prompt = read_prompt_from_markdown_with_validation(vision_markdown_file_path)
    chat_prompt = read_prompt_from_markdown_with_validation(chat_markdown_file_path)

    for image_filename in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_filename)
        if os.path.isfile(image_path):
            try:
                # Process each image with the vision model
                vision_prompt_uuid = prompt_db.add_entry(prompt=vision_prompt, prompt_role="Vision Model")
                response_text = generate_content_from_image(image_path, vision_prompt, generation_config)
                response_uuid = str(uuid4())

                if response_text == "Failed to receive a valid response after multiple attempts.":
                    logging.error(f"Failed to generate content for {image_path}")
                    continue

                # Process the chat model
                chat_prompt_uuid = prompt_db.add_entry(prompt=chat_prompt, prompt_role="Chat Model")
                chat_session = ChatSession(model_name=model_name, generation_config=chat_generation_config)
                chat_response = chat_session.send_message(f"Image: {image_path}, Response: {response_text}, Prompt: {chat_prompt}")
                overlay_suggestion = chat_response.text

                db.add_entry(file_name=image_filename, response=response_text,
                             prompt_uuid=vision_prompt_uuid, response_uuid=response_uuid,
                             image_path_url=image_path, overlay_suggestion=overlay_suggestion)

                logging.info(f"Processed {image_path} successfully with overlay suggestion: {overlay_suggestion}")
            except Exception as e:
                logging.error(f"Error processing {image_path}: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="process_log.txt", filemode="a",
                        format="%(asctime)s - %(levelname)s - %(message)s")
    image_folder_path = 'response'  # Folder containing images
    vision_markdown_file_path = '_prompts/extract_product_details.md'
    chat_markdown_file_path = '_prompts/chat/v1.md'
    generation_config_path = 'gemini/config_choice/vision_config.json'  # Path to the vision generation configuration
    chat_config_path = 'gemini/config_choice/pro_config.json'  # Path to the chat configuration

    generation_config = load_generation_config(generation_config_path)
    model_name, chat_generation_config = load_chat_config(chat_config_path)

    process_images_in_folder(image_folder_path, vision_markdown_file_path, chat_markdown_file_path, generation_config, chat_generation_config, model_name)
