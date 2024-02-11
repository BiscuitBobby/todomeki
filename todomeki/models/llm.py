import google.generativeai as genai
from todomeki.models.config.gemini import safety_settings


class GeminiPro:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)

        generation_config = {
            "temperature": 0.2,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }

        self.model = genai.GenerativeModel(
            model_name='gemini-pro',
            generation_config=generation_config,
            safety_settings=safety_settings
        )
