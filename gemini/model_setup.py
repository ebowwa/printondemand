from pydantic import BaseModel, Field
import google.generativeai as genai

class GenerationConfig(BaseModel):
    temperature: float = Field(default=0.75, ge=0, le=1)
    top_p: float = Field(default=1, ge=0, le=1)
    top_k: int = Field(default=32, ge=0)
    max_output_tokens: int = Field(default=4096, ge=1)

class SafetySetting(BaseModel):
    category: str
    threshold: str

class ConfigureGenAI(BaseModel):
    api_key: str
    gen_model_name: str = "gemini-pro-vision"  
    generation_config: GenerationConfig
    safety_settings: list[SafetySetting]

def configure_genai(api_key: str):
    genai.configure(api_key=api_key)
  
    generation_config = GenerationConfig()
    safety_settings = [
        SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE"),
        SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"),
        SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_NONE"),
        SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_NONE"),
    ]
  
    config = ConfigureGenAI(api_key=api_key,
                            gen_model_name="gemini-pro-vision",  
                            generation_config=generation_config,
                            safety_settings=safety_settings)
  
    model = genai.GenerativeModel(model_name=config.gen_model_name,  
                                  generation_config=config.generation_config.dict(),
                                  safety_settings=[setting.dict() for setting in config.safety_settings])
    return model