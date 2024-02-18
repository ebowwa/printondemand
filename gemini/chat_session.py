# gemini/chat_session.py
from concurrent.futures import ThreadPoolExecutor
import os
from .model_setup import configure_genai
from .auth_gemini import get_api_key

class ChatSession:
    def __init__(self, model_name=None, generation_config=None):
        api_key = get_api_key()
        # If model_name is None, configure_genai will use its default
        # If generation_config is None, configure_genai should handle default internally
        self.model = configure_genai(api_key=api_key, gen_model_name=model_name, generation_config=generation_config)
        self.chat_session = None
        self.executor = ThreadPoolExecutor(max_workers=os.cpu_count())

    def start_chat(self, history=None):
        self.chat_session = self.model.start_chat(history=history)
        return self.chat_session

    def send_message(self, content, **kwargs):
        if self.chat_session is None:
            self.start_chat()
        response = self.chat_session.send_message(content, **kwargs)
        return response

    def rewind(self):
        if self.chat_session is not None:
            return self.chat_session.rewind()
        else:
            raise Exception("Chat session not started.")

    def send_message_async(self, content, **kwargs):
        future = self.executor.submit(self.send_message, content, **kwargs)
        return future.result()

    def __del__(self):
      if hasattr(self, 'executor'):
          self.executor.shutdown(wait=True)
  
  