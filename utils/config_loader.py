# utils/config_loader.py
import json

def load_generation_config(config_path='gemini/config_choice/vision_config.json'):
    with open(config_path, 'r') as file:
        return json.load(file)["generation_config"]

def load_chat_config(config_path='gemini/config_choice/pro_config.json'):
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    model_name = config.get("generation_config", {}).pop("gen_model_name", None)
    chat_generation_config = config.get("generation_config", {})
    return model_name, chat_generation_config
