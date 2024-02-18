# gemini/model_setup.py
from pydantic import BaseModel, Field
import google.generativeai as genai
from .safety import SafetySetting, SAFETY_THRESHOLDS

class GenerationConfig(BaseModel):
    temperature: float = Field(default=0.75, ge=0, le=1)
    top_p: float = Field(default=0, ge=0, le=1)
    top_k: int = Field(default=32, ge=0)
    max_output_tokens: int = Field(default=4096, ge=1)

class ConfigureGenAI(BaseModel):
    api_key: str
    gen_model_name: str = Field(default=None)
    generation_config: GenerationConfig
    safety_settings: list[SafetySetting]

def configure_genai(api_key: str, gen_model_name: str, generation_config: dict):
    genai.configure(api_key=api_key)

    gen_config = GenerationConfig(**generation_config)
    safety_settings = [
        SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold=SAFETY_THRESHOLDS["Block none"]),
        SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold=SAFETY_THRESHOLDS["Block none"]),
        SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold=SAFETY_THRESHOLDS["Block none"]),
        SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold=SAFETY_THRESHOLDS["Block none"]),
    ]

    config = ConfigureGenAI(api_key=api_key,
                            gen_model_name=gen_model_name,  
                            generation_config=gen_config,
                            safety_settings=safety_settings)

    model = genai.GenerativeModel(model_name=config.gen_model_name,  
                                  generation_config=config.generation_config.dict(),
                                  safety_settings=[setting.dict() for setting in config.safety_settings])
    return model
