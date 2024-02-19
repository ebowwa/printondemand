import logging
import os
from uuid import uuid4
from utils.config_loader import load_generation_config, load_chat_config
from utils.initializer import initialize_directories, initialize_databases
from utils.read_prompt import read_prompt_from_markdown_with_validation
from vision import generate_content_from_image
from gemini.chat_session import ChatSession

def process_image(image_path, vision_prompt, generation_config, chat_prompt, chat_generation_config, model_name, prompt_db, db):
    try:
        vision_prompt_uuid = prompt_db.add_entry(prompt=vision_prompt, prompt_role="Vision Model")
        response_text = generate_content_from_image(image_path, vision_prompt, generation_config)
        response_uuid = str(uuid4())

        if response_text == "Failed to receive a valid response after multiple attempts.":
            logging.error(f"Failed to generate content for {image_path}")
            return

        chat_prompt_uuid = prompt_db.add_entry(prompt=chat_prompt, prompt_role="Chat Model")
        chat_session = ChatSession(model_name=model_name, generation_config=chat_generation_config)
        chat_response = chat_session.send_message(f"Image: {image_path}, Response: {response_text}, Prompt: {chat_prompt}")
        overlay_suggestion = chat_response.text

        db.add_entry(file_name=os.path.basename(image_path), response=response_text,
                     prompt_uuid=vision_prompt_uuid, response_uuid=response_uuid,
                     image_path_url=image_path, overlay_suggestion=overlay_suggestion)

        logging.info(f"Processed {image_path} successfully with overlay suggestion: {overlay_suggestion}")
    except Exception as e:
        logging.error(f"Error processing {image_path}: {e}")

def main_process(folder_path, vision_markdown_file_path, chat_markdown_file_path, dir_name, db, prompt_db, generation_config, chat_generation_config, model_name):
    vision_prompt = read_prompt_from_markdown_with_validation(vision_markdown_file_path)
    chat_prompt = read_prompt_from_markdown_with_validation(chat_markdown_file_path)

    for image_filename in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_filename)
        if os.path.isfile(image_path):
            process_image(image_path, vision_prompt, generation_config, chat_prompt, chat_generation_config, model_name, prompt_db, db)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="process_log.txt", filemode="a",
                        format="%(asctime)s - %(levelname)s - %(message)s")

    image_folder_path = 'response'
    vision_markdown_file_path = '_prompts/extract_product_details.md'
    chat_markdown_file_path = '_prompts/chat/v1.md'
    generation_config_path = 'gemini/config_choice/vision_config.json'
    chat_config_path = 'gemini/config_choice/pro_config.json'

    generation_config = load_generation_config(generation_config_path)
    model_name, chat_generation_config = load_chat_config(chat_config_path)
    dir_name = initialize_directories()
    db, prompt_db = initialize_databases(dir_name)

    main_process(image_folder_path, vision_markdown_file_path, chat_markdown_file_path, dir_name, db, prompt_db, generation_config, chat_generation_config, model_name)
