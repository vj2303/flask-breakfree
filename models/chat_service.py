from typing import Dict
from datetime import datetime
import google.generativeai as genai
from config.settings import Config


class ChatService:
    """Service for generating responses using Gemini based on a profile."""

    @staticmethod
    def _build_generation_config(profile: Dict) -> dict:
        return {
            "temperature": profile.get("temperature", 0.7),
            "top_k": profile.get("top_k", 40),
            "top_p": profile.get("top_p", 0.9),
            "max_output_tokens": profile.get("max_output_tokens", 2048),
        }

    @staticmethod
    def generate(profile: Dict, message: str) -> Dict:
        genai.configure(api_key=Config.GEMINI_API_KEY)

        model = genai.GenerativeModel(
            model_name=profile["model"],
            generation_config=genai.types.GenerationConfig(**ChatService._build_generation_config(profile)),
            system_instruction=profile["system_instruction"],
        )

        response = model.generate_content(message)

        return {
            "profile_used": {
                "id": profile["id"],
                "title": profile["title"],
                "model": profile["model"],
            },
            "user_message": message,
            "ai_response": response.text,
            "timestamp": datetime.now().isoformat(),
        }

    @staticmethod
    def generate_stream(profile: Dict, message: str) -> Dict:
        genai.configure(api_key=Config.GEMINI_API_KEY)

        model = genai.GenerativeModel(
            model_name=profile["model"],
            generation_config=genai.types.GenerationConfig(**ChatService._build_generation_config(profile)),
            system_instruction=profile["system_instruction"],
        )

        response = model.generate_content(message, stream=True)

        full_response = ""
        for chunk in response:
            if getattr(chunk, "text", None):
                full_response += chunk.text

        return {
            "profile_used": {
                "id": profile["id"],
                "title": profile["title"],
                "model": profile["model"],
            },
            "user_message": message,
            "ai_response": full_response,
            "timestamp": datetime.now().isoformat(),
        }


