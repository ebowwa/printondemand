import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

load_dotenv()  # This loads the .env file at the project root

class Settings(BaseModel):
   gemini_api_key: str = Field(default="YOUR_API_KEY", env="GEMINI_API_KEY")

def get_api_key() -> str:
    try:
        settings = Settings()  # This will automatically load the GEMINI_API_KEY from environment variables
        api_key = settings.gemini_api_key
        if api_key == "YOUR_API_KEY":
            raise ValueError("""
                You haven't set up your API key yet.

                If you don't already have one, create a key with in Google AI Studio:

                https://makersuite.google.com/app/apikey

                Then, open the Secrets Tool and add GEMINI_API_KEY as a secret.
            """)
        return api_key
    except ValidationError as e:
        raise ValueError(f"Error loading configuration: {e}")

# Usage example
if __name__ == "__main__":
    try:
        api_key = get_api_key()
        print(f"API Key: {api_key}")
    except ValueError as e:
        print(e)
