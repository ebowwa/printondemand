# 1. take webp ✅
# 2. convert to png ✅
## send to Gemini to write SEO for product marketing 

## with GEMINI
# 1.)  have gemini name image 
# 2.)  have gemini write all the product details
# #.) (Optional) Upscale Images and resize appropriately i.e 4500x5400
# 4.) submit to Amazon

## uuid tracking system of gemini responses, images, prompts


# main.py using the WebpToPngConverter with UUID naming
import csv
from webp2png import WebpToPngConverter  # Ensure this is correctly imported
from vision import generate_content_from_image  # Adjust import path as necessary

def read_prompt_from_markdown(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

def log_api_response(log_file_path, original_filename, uuid_filename, summary):
    with open(log_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([original_filename, uuid_filename, summary])

def main():
    prompt = read_prompt_from_markdown('_prompts/extract_product_details.md')
    log_file_path = 'log.csv'
    source_directory_path = 'unzipped_content/discord_Midjorneyv6'
    target_directory_path = 'response'

    converter = WebpToPngConverter(source_directory_path, target_directory_path)
    conversion_details = converter.convert_all()

    for file_detail in conversion_details:
        try:
            response_text = generate_content_from_image(file_detail['file_path'], prompt)
            print(f"API response for {file_detail['uuid_filename']}: {response_text}")
            log_api_response(log_file_path, file_detail['original_filename'], file_detail['uuid_filename'], "Success/Summary")
        except ValueError as e:
            print(f"Error processing the response for {file_detail['uuid_filename']}: {e}")
            log_api_response(log_file_path, file_detail['original_filename'], file_detail['uuid_filename'], "Error")

if __name__ == "__main__":
    main()
