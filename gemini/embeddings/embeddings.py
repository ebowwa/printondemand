# embeddings.py
from google.api_core import retry
import google.generativeai as genai
import numpy as np
from tqdm.auto import tqdm
from gemini.auth_gemini import get_api_key  # Import get_api_key

def configure_api():
    api_key = get_api_key()  # Use get_api_key to obtain the API key
    genai.configure(api_key=api_key)  # Configure the API with the obtained key

def create_embeddings(df, model='models/embedding-001'):
    configure_api()  # Ensure the API is configured with the correct key before creating embeddings
    tqdm.pandas()

    def make_embed_text_fn(model):
        @retry.Retry(timeout=300.0)
        def embed_fn(text: str) -> list[float]:
            embedding = genai.embed_content(model=model, content=text, task_type="clustering")['embedding']
            return np.array(embedding)
        return embed_fn

    df['Embeddings'] = df['Text'].progress_apply(make_embed_text_fn(model))
    df.drop('index', axis=1, inplace=True)
    return df
