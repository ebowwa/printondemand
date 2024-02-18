# Import necessary classes from response_handler.py
# from gemini.response_handler import FinishReason, SafetyRating, GroundingPassageId, SemanticRetrieverChunk, AttributionSourceId, GroundingAttribution, CitationSource, CitationMetadata, ResponseCandidate
import PIL.Image
import time
from gemini.model_setup import configure_genai
from gemini.auth_gemini import get_api_key

def generate_content_from_image(image_path, prompt, gen_model_name, max_retries=3):
    api_key = get_api_key()
    model = configure_genai(api_key, gen_model_name)
    img = PIL.Image.open(image_path)
    retry_count = 0

    while retry_count < max_retries:
        response = model.generate_content([prompt, img])

        # Handle multipart response
        if hasattr(response, 'parts'):
            response_text = ''.join(part.text for part in response.parts)
        else:
            response_text = response.text

        if response_text.strip():
            return response_text
        else:
            print("Received an empty response, retrying...")
            retry_count += 1
            time.sleep(1)  # Wait for 1 second before retrying

    # If max retries reached and still empty, return a notice or handle as needed
    return "Failed to receive a valid response after multiple attempts."

if __name__ == "__main__":
    def read_prompt_from_markdown(file_path):
        with open(file_path, 'r') as file:
            return file.read().strip()

    def main():
        gen_model_name = "gemini-pro-vision"
        image_path = 'response/5bdf859e-ea13-4806-b807-174b7f34f9a3.png'
        prompt = read_prompt_from_markdown('_prompts/extract_product_details.md')

        try:
            response_text = generate_content_from_image(image_path, prompt, gen_model_name)
            if response_text != "Failed to receive a valid response after multiple attempts.":
                print(response_text)
            else:
                # Handle failure case, could log or take alternative action
                print("Unable to generate content from image after several attempts.")
        except ValueError as e:
            print(f"Error processing the response: {e}")

    main()
