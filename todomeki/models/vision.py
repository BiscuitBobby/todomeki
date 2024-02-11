import google.generativeai as genai
from todomeki.models.config.gemini import safety_settings


class GeminiProVision:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)

        vision_generation_config = {
            "temperature": 0.3,
            "top_p": 1,
            "top_k": 32,
            "max_output_tokens": 4096,
        }

        self.model = genai.GenerativeModel(
            model_name="gemini-pro-vision",
            generation_config=vision_generation_config,
            safety_settings=safety_settings
        )
