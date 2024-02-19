import os
import json
from datetime import datetime
from vision import generate_content_from_image  # Ensure this is your vision model's import path
from uuid import uuid4
from uuid_track.uuid_database import UUIDDatabase
from uuid_track.prompt_database import PromptDatabase
from gemini.chat_session import ChatSession  # Ensure this is your chat model's import path
from utils.read_prompt import read_prompt_from_markdown, ReadPromptRequest, read_prompt_from_markdown_with_validation  # Adjusted import
from utils.config_loader import load_generation_config, load_chat_config
from utils.initializer import initialize_directories, initialize_databases

def process_image_and_chat(image_path, vision_prompt, chat_prompt, generation_config, chat_generation_config, dir_name):
    # Vision Model Prompt
    vision_prompt_uuid = prompt_db.add_entry(prompt=vision_prompt, prompt_role="Vision Model")  # Specify role

    # Generate content from image with Model A
    response_text = generate_content_from_image(image_path, vision_prompt, generation_config)
    response_uuid = str(uuid4())

    if response_text == "Failed to receive a valid response after multiple attempts.":
        print("Unable to generate content from image after several attempts.")
        return

    # Chat Model Prompt
    chat_prompt_uuid = prompt_db.add_entry(prompt=chat_prompt, prompt_role="Chat Model")  # Specify role

    # Initialize Chat Session for Model B with additional context
    chat_session = ChatSession(model_name=model_name, generation_config=chat_generation_config)
    chat_response = chat_session.send_message(f"Image: {image_path}, Response: {response_text}, Prompt: {chat_prompt}")
    overlay_suggestion = chat_response.text

    db.add_entry(file_name=image_path, response=response_text, prompt_uuid=vision_prompt_uuid, response_uuid=response_uuid, image_path_url=image_path, overlay_suggestion=overlay_suggestion)

    print(f"Vision Model Response: {response_text}\nOverlay Suggestion: {overlay_suggestion}")

# Initialize directories and databases
dir_name = initialize_directories()
db, prompt_db = initialize_databases(dir_name)

# Load configurations
generation_config = load_generation_config()
model_name, chat_generation_config = load_chat_config()

# Specify image and markdown file paths
image_path = 'response/00c90244-64ea-49fa-b26b-63394a92a088.png'
vision_markdown_file_path = '_prompts/extract_product_details.md'
chat_markdown_file_path = '_prompts/chat/v1.md'

# Read prompts from markdown files using the adjusted function
vision_prompt = read_prompt_from_markdown_with_validation(vision_markdown_file_path)
chat_prompt = read_prompt_from_markdown_with_validation(chat_markdown_file_path)

if __name__ == "__main__":
    process_image_and_chat(image_path, vision_prompt, chat_prompt, generation_config, chat_generation_config, dir_name)
