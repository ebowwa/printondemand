# vision.py
import json
import PIL.Image
import time
from gemini.model_setup import configure_genai
from gemini.auth_gemini import get_api_key

def generate_content_from_image(image_path, prompt, generation_config, max_retries=3):
    api_key = get_api_key()
    # Directly access gen_model_name; do not modify the original dict
    gen_model_name = generation_config.get('gen_model_name')
    if not gen_model_name:
        raise ValueError("Model name not specified in generation configuration.")
    # Pass a copy of generation_config without the gen_model_name to configure_genai
    config_without_model_name = {key: val for key, val in generation_config.items() if key != 'gen_model_name'}
    model = configure_genai(api_key, gen_model_name, config_without_model_name)
    img = PIL.Image.open(image_path)
    retry_count = 0

    while retry_count < max_retries:
        response = model.generate_content([prompt, img])
        if hasattr(response, 'parts'):
            response_text = ''.join(part.text for part in response.parts)
        else:
            response_text = response.text
        if response_text.strip():
            return response_text
        else:
            print("Received an empty response, retrying...")
            retry_count += 1
            time.sleep(1)

    return "Failed to receive a valid response after multiple attempts."

    
if __name__ == "__main__":
    def read_prompt_from_markdown(file_path):
        with open(file_path, 'r') as file:
            return file.read().strip()

    def load_generation_config(config_path):
        with open(config_path, 'r') as file:
            return json.load(file)["generation_config"]

    def main():
        generation_config = load_generation_config('gemini/vision_config.json')
        image_path = 'response/5bdf859e-ea13-4806-b807-174b7f34f9a3.png'
        prompt = read_prompt_from_markdown('_prompts/extract_product_details.md')

        try:
            response_text = generate_content_from_image(image_path, prompt, generation_config)
            if response_text != "Failed to receive a valid response after multiple attempts.":
                print(response_text)
            else:
                print("Unable to generate content from image after several attempts.")
        except ValueError as e:
            print(f"Error processing the response: {e}")

    main()
