# from flask import Blueprint, jsonify
# from controllers import get_all_users

# main_blueprint = Blueprint('main', __name__)

# @main_blueprint.route('/users')
# def users():
#     users = get_all_users()
#     return jsonify([
#         {'id': user.id, 'username': user.username, 'email': user.email}
#         for user in users
#     ]) 

# application/routes/__init__.py
from .llmwork import LLM

__all__ = ["LLM"]
