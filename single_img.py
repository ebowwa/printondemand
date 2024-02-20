# single_img.py
import os
import json
from datetime import datetime
from vision import generate_content_from_image  # Ensure this is your vision model's import path
from uuid import uuid4
from uuid_track.uuid_database import UUIDDatabase
from uuid_track.prompt_database import PromptDatabase
from gemini.chat_session import ChatSession  # Ensure this is your chat model's import path
from utils.read_prompt import read_prompt_from_markdown_with_validation  # Adjusted import
from utils.config_loader import load_generation_config, load_chat_config
from utils.initializer import initialize_directories, initialize_databases

def process_image_and_chat(image_path, vision_prompt, chat_prompt, generation_config, chat_generation_config, dir_name, db, prompt_db, model_name):
  vision_prompt_uuid = prompt_db.add_entry(prompt=vision_prompt, prompt_role="Vision Model")
  vision_response_uuid = str(uuid4())

  vision_response = generate_content_from_image(image_path, vision_prompt, generation_config)

  if vision_response == "Failed to receive a valid response after multiple attempts.":
      print("Unable to generate content from image after several attempts.")
      return

  chat_prompt_uuid = prompt_db.add_entry(prompt=chat_prompt, prompt_role="Chat Model")
  chat_response_uuid = str(uuid4())

  chat_session = ChatSession(model_name=model_name, generation_config=chat_generation_config)
  chat_response = chat_session.send_message(f"Image: {image_path}, Response: {vision_response}, Prompt: {chat_prompt}")

  db.add_entry(file_name=image_path, vision_response=vision_response, chat_response=chat_response.text, vision_prompt_uuid=vision_prompt_uuid, chat_prompt_uuid=chat_prompt_uuid, vision_response_uuid=vision_response_uuid, chat_response_uuid=chat_response_uuid, image_path_url=image_path, overlay_suggestion=chat_response.text)

  print(f"Vision Model Response: {vision_response}\nChat Response: {chat_response.text}")

if __name__ == "__main__":
    dir_name = initialize_directories()
    db, prompt_db = initialize_databases(dir_name)
    generation_config = load_generation_config()
    model_name, chat_generation_config = load_chat_config()
    image_path = 'response/00c90244-64ea-49fa-b26b-63394a92a088.png'
    vision_markdown_file_path = '_prompts/product/extract_product_details.md'
    chat_markdown_file_path = '_prompts/chat/v1.md'
    vision_prompt = read_prompt_from_markdown_with_validation(vision_markdown_file_path)
    chat_prompt = read_prompt_from_markdown_with_validation(chat_markdown_file_path)

    process_image_and_chat(image_path, vision_prompt, chat_prompt, generation_config, chat_generation_config, dir_name, db, prompt_db, model_name)


# make polymorphic so that this can be imported higher level and used with a folder of images rather than just one