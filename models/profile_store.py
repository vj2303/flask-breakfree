from typing import Dict, List, Optional


class ProfileStore:
    """Simple in-memory profile store. In production, replace with a database."""

    _profiles: Dict[int, dict] = {}
    _counter: int = 1

    @classmethod
    def seed_defaults(cls):
        if cls._profiles:
            return
        cls._profiles[1] = {
            "id": 1,
            "title": "Creative Writer",
            "system_instruction": (
                "You are a creative writing assistant. Help users write engaging "
                "stories, poems, and creative content with vivid descriptions and "
                "compelling narratives."
            ),
            "model": "gemini-1.5-pro",
            "temperature": 0.9,
            "top_k": 40,
            "top_p": 0.9,
            "max_output_tokens": 2048,
            "created_at": "",
            "updated_at": "",
        }
        cls._profiles[2] = {
            "id": 2,
            "title": "Code Assistant",
            "system_instruction": (
                "You are a programming assistant. Help users write clean, efficient "
                "code and explain programming concepts clearly. Always provide "
                "working examples."
            ),
            "model": "gemini-1.5-flash",
            "temperature": 0.2,
            "top_k": 20,
            "top_p": 0.8,
            "max_output_tokens": 2048,
            "created_at": "",
            "updated_at": "",
        }
        cls._counter = 3

    @classmethod
    def list_profiles(cls) -> List[dict]:
        return list(cls._profiles.values())

    @classmethod
    def get_profile(cls, profile_id: int) -> Optional[dict]:
        return cls._profiles.get(profile_id)

    @classmethod
    def create_profile(cls, profile_data: dict) -> dict:
        profile_id = cls._counter
        profile = {"id": profile_id, **profile_data}
        cls._profiles[profile_id] = profile
        cls._counter += 1
        return profile

    @classmethod
    def update_profile(cls, profile_id: int, updates: dict) -> dict:
        cls._profiles[profile_id] = {**cls._profiles[profile_id], **updates}
        return cls._profiles[profile_id]

    @classmethod
    def delete_profile(cls, profile_id: int) -> dict:
        return cls._profiles.pop(profile_id)


