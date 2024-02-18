# main.py

import os
from datetime import datetime
from vision import generate_content_from_image  # Updated to support gen_model_name
from uuid import uuid4
from uuid_track.uuid_database import UUIDDatabase
from uuid_track.prompt_database import PromptDatabase  

def main():
    run_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dir_name = f"data_{run_time}"
    os.makedirs(dir_name, exist_ok=True)

    db = UUIDDatabase(f'{dir_name}/uuid_data.csv')
    prompt_db = PromptDatabase(f'{dir_name}/prompt_data.csv')

    image_path = 'response/5bdf859e-ea13-4806-b807-174b7f34f9a3.png'
    markdown_file_path = '_prompts/extract_product_details.md'
    model_name = "gemini-pro-vision"  # Specify the model name here

    def read_prompt_from_markdown(file_path):
        with open(file_path, 'r') as file:
            return file.read().strip()

    prompt = read_prompt_from_markdown(markdown_file_path)
    prompt_uuid = str(uuid4())
    prompt_uuid = prompt_db.add_entry(prompt=prompt)

    # Pass model_name as an argument
    response_text = generate_content_from_image(image_path, prompt, model_name)
    response_uuid = str(uuid4())

    if response_text == "Failed to receive a valid response after multiple attempts.":
        print("Unable to generate content from image after several attempts.")
        return

    db.add_entry(file_name=image_path, response=response_text,
                 prompt_uuid=prompt_uuid, response_uuid=response_uuid, image_path_url=image_path)

    print(f"Response length: {len(response_text)} characters")
    print(response_text)

if __name__ == "__main__":
    main()


    # Example query by Prompt UUID
#    entries_by_prompt_uuid = db.search_entries({'Prompt UUID': prompt_uuid})
#    print(entries_by_prompt_uuid)
# Add an entry
# db.add_entry('file1.txt', 'What is Python?', 'Python is a programming language.', 'prompt_uuid_1', 'response_uuid_1', 'A')

# Search entries
# results = db.search_entries({'Grade': 'A'})

# Update an entry's grade
# success = db.update_grade('prompt_uuid_1', 'A+')


# NEED: add png or png link to csv
