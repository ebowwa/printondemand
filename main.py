from vision import generate_content_from_image
from uuid import uuid4
from uuid_track.uuid_database import UUIDDatabase  

def main():
    # Initialize the UUIDDatabase
    db = UUIDDatabase('uuid_data.csv')  # Specify your CSV file path

    image_path = 'response/5bdf859e-ea13-4806-b807-174b7f34f9a3.png'
    markdown_file_path = '_prompts/extract_product_details.md'

    def read_prompt_from_markdown(file_path):
        with open(file_path, 'r') as file:
            return file.read().strip()

    prompt = read_prompt_from_markdown(markdown_file_path)
    prompt_uuid = str(uuid4())  # Generate a UUID for the prompt

    response_text = generate_content_from_image(image_path, prompt)
    response_uuid = str(uuid4())  # Generate a UUID for the response

    if response_text == "Failed to receive a valid response after multiple attempts.":
        print("Unable to generate content from image after several attempts.")
        return

    # Save the response in the database
    db.add_entry(file_name=image_path, prompt=prompt, response=response_text,
                 prompt_uuid=prompt_uuid, response_uuid=response_uuid)

    # Output the generated content
    total_length = len(response_text)
    print(f"Response length: {total_length} characters")
    print(response_text)

    # Example query by Prompt UUID
#    entries_by_prompt_uuid = db.search_entries({'Prompt UUID': prompt_uuid})
#    print(entries_by_prompt_uuid)

#   save a csv 
#   - with the response(include the response uuid and prompt uuid, and a response uuid)
#   - be relational and efficient
#   - be able to query by uuid
#   - be able to query by prompt uuid
#   - be able to query by response uuid
#   - be able to query by prompt and response uuid
#   - be able to query by Grade
#   - be able to query by prompt and Grade

if __name__ == "__main__":
    main()