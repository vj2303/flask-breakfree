from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from controllers.video_controller import VideoController

video_bp = Blueprint('video', __name__)

@video_bp.route('/evaluate-interview', methods=['POST'])
def evaluate_interview():
    """Endpoint for evaluating interview videos with structured metrics"""
    return VideoController.evaluate_interview(request)

@video_bp.route('/analyze-video', methods=['POST'])
def analyze_video():
    """Endpoint for general video analysis with custom prompts"""
    return VideoController.analyze_video(request)