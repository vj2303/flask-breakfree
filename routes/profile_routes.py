from flask import Blueprint, request, jsonify
from controllers.profile_controller import ProfileController
from models.profile_store import ProfileStore
from models.chat_service import ChatService


profile_bp = Blueprint('profiles', __name__)


@profile_bp.route('/', methods=['GET'])
def home():
    return ProfileController.home()


@profile_bp.route('/models', methods=['GET'])
def get_models():
    return ProfileController.get_models()


@profile_bp.route('/profiles', methods=['GET'])
def list_profiles():
    return ProfileController.list_profiles()


@profile_bp.route('/profiles/<int:profile_id>', methods=['GET'])
def get_profile(profile_id: int):
    return ProfileController.get_profile(profile_id)


@profile_bp.route('/profiles', methods=['POST'])
def create_profile():
    payload = request.get_json() or {}
    return ProfileController.create_profile(payload)


@profile_bp.route('/profiles/<int:profile_id>', methods=['PUT'])
def update_profile(profile_id: int):
    payload = request.get_json() or {}
    return ProfileController.update_profile(profile_id, payload)


@profile_bp.route('/profiles/<int:profile_id>', methods=['DELETE'])
def delete_profile(profile_id: int):
    return ProfileController.delete_profile(profile_id)


@profile_bp.route('/chat', methods=['POST'])
def chat_with_profile():
    data = request.get_json() or {}
    if 'profile_id' not in data:
        return jsonify({"error": "Missing profile_id"}), 400
    if 'message' not in data:
        return jsonify({"error": "Missing message"}), 400

    profile = ProfileStore.get_profile(int(data['profile_id']))
    if profile is None:
        return jsonify({"error": "Profile not found"}), 404

    result = ChatService.generate(profile, data['message'])
    return jsonify(result)


@profile_bp.route('/chat/stream', methods=['POST'])
def stream_chat():
    data = request.get_json() or {}
    if 'profile_id' not in data or 'message' not in data:
        return jsonify({"error": "Missing profile_id or message"}), 400

    profile = ProfileStore.get_profile(int(data['profile_id']))
    if profile is None:
        return jsonify({"error": "Profile not found"}), 404

    result = ChatService.generate_stream(profile, data['message'])
    return jsonify(result)


# Seed defaults at import time so that GET /profiles has initial data
ProfileStore.seed_defaults()


