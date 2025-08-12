from datetime import datetime
from flask import jsonify
from models.profile_store import ProfileStore


class ProfileController:
    """Controller for managing AI profiles and related metadata."""

    AVAILABLE_MODELS = [
        "gemini-1.5-pro",
        "gemini-1.5-flash",
        "gemini-1.0-pro",
        "gemini-pro-vision",
    ]

    @staticmethod
    def home():
        return jsonify({
            "message": "Gemini AI Profile Manager API",
            "endpoints": {
                "GET /profiles": "List all profiles",
                "POST /profiles": "Create a new profile",
                "GET /profiles/<id>": "Get specific profile",
                "PUT /profiles/<id>": "Update profile",
                "DELETE /profiles/<id>": "Delete profile",
                "POST /chat": "Chat using a specific profile",
                "POST /chat/stream": "Stream chat using a specific profile",
                "GET /models": "List available Gemini models",
            },
        })

    @staticmethod
    def get_models():
        return jsonify({"available_models": ProfileController.AVAILABLE_MODELS})

    @staticmethod
    def list_profiles():
        profiles = ProfileStore.list_profiles()
        return jsonify({"profiles": profiles, "total": len(profiles)})

    @staticmethod
    def get_profile(profile_id: int):
        profile = ProfileStore.get_profile(profile_id)
        if profile is None:
            return jsonify({"error": "Profile not found"}), 404
        return jsonify(profile)

    @staticmethod
    def create_profile(payload: dict):
        # Validate required fields
        required_fields = ["title", "system_instruction"]
        for field in required_fields:
            if field not in payload:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Validate model
        model = payload.get("model", "gemini-1.5-pro")
        if model not in ProfileController.AVAILABLE_MODELS:
            return jsonify({
                "error": f"Invalid model. Available models: {ProfileController.AVAILABLE_MODELS}"
            }), 400

        # Parameters with defaults
        temperature = payload.get("temperature", 0.7)
        top_k = payload.get("top_k", 40)
        top_p = payload.get("top_p", 0.9)
        max_output_tokens = payload.get("max_output_tokens", 2048)

        # Validate params
        if not (0 <= float(temperature) <= 2):
            return jsonify({"error": "Temperature must be between 0 and 2"}), 400
        if not (1 <= int(top_k) <= 100):
            return jsonify({"error": "top_k must be between 1 and 100"}), 400
        if not (0 <= float(top_p) <= 1):
            return jsonify({"error": "top_p must be between 0 and 1"}), 400

        new_profile = {
            "title": payload["title"],
            "system_instruction": payload["system_instruction"],
            "model": model,
            "temperature": float(temperature),
            "top_k": int(top_k),
            "top_p": float(top_p),
            "max_output_tokens": int(max_output_tokens),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }

        created = ProfileStore.create_profile(new_profile)
        return jsonify({"message": "Profile created successfully", "profile": created}), 201

    @staticmethod
    def update_profile(profile_id: int, payload: dict):
        existing = ProfileStore.get_profile(profile_id)
        if existing is None:
            return jsonify({"error": "Profile not found"}), 404

        updates = {}
        if "title" in payload:
            updates["title"] = payload["title"]
        if "system_instruction" in payload:
            updates["system_instruction"] = payload["system_instruction"]
        if "model" in payload:
            if payload["model"] not in ProfileController.AVAILABLE_MODELS:
                return jsonify({
                    "error": f"Invalid model. Available models: {ProfileController.AVAILABLE_MODELS}"
                }), 400
            updates["model"] = payload["model"]
        if "temperature" in payload:
            if not (0 <= float(payload["temperature"]) <= 2):
                return jsonify({"error": "Temperature must be between 0 and 2"}), 400
            updates["temperature"] = float(payload["temperature"])
        if "top_k" in payload:
            if not (1 <= int(payload["top_k"]) <= 100):
                return jsonify({"error": "top_k must be between 1 and 100"}), 400
            updates["top_k"] = int(payload["top_k"])
        if "top_p" in payload:
            if not (0 <= float(payload["top_p"]) <= 1):
                return jsonify({"error": "top_p must be between 0 and 1"}), 400
            updates["top_p"] = float(payload["top_p"])
        if "max_output_tokens" in payload:
            updates["max_output_tokens"] = int(payload["max_output_tokens"])

        updates["updated_at"] = datetime.now().isoformat()
        updated = ProfileStore.update_profile(profile_id, updates)
        return jsonify({"message": "Profile updated successfully", "profile": updated})

    @staticmethod
    def delete_profile(profile_id: int):
        existing = ProfileStore.get_profile(profile_id)
        if existing is None:
            return jsonify({"error": "Profile not found"}), 404
        deleted = ProfileStore.delete_profile(profile_id)
        return jsonify({"message": "Profile deleted successfully", "deleted_profile": deleted})


