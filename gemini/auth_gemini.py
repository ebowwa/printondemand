# gemini/auth_gemini.py
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

class Settings(BaseModel):
   gemini_api_key: str = Field(default="AIzaSyAytlE899-HFzODphPxUpIWKaNBQ-PXTqs", env="GEMINI_API_KEY")
#   gemini_api_key: str = Field(default="YOUR_API_KEY", env="GEMINI_API_KEY")

def get_api_key() -> str:
    settings = Settings()
    if settings.gemini_api_key == "YOUR_API_KEY":
        raise ValueError("""
            You haven't set up your API key yet.

            If you don't already have one, create a key with in Google AI Studio:

            https://makersuite.google.com/app/apikey

            Then, open the Secrets Tool and add GEMINI_API_KEY as a secret.
        """)
    return settings.gemini_api_key

