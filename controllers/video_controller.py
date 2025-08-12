from flask import jsonify
from werkzeug.utils import secure_filename
from models.video_analyzer import VideoAnalyzer
from models.interview_evaluator import InterviewEvaluator
from utils.file_validator import FileValidator
from utils.response_parser import ResponseParser

class VideoController:
    
    @staticmethod
    def evaluate_interview(request):
        """Handle interview evaluation requests"""
        try:
            # Validate request has video file
            if 'video' not in request.files:
                return jsonify({'error': 'No video file provided'}), 400
            
            video_file = request.files['video']
            
            # Validate file
            validation_error = FileValidator.validate_video_file(video_file)
            if validation_error:
                return validation_error
            
            # Read video bytes
            video_bytes = video_file.read()
            
            # Check file size
            if len(video_bytes) > 100 * 1024 * 1024:  # 100MB
                return jsonify({'error': 'File size exceeds 100MB limit'}), 400
            
            # Get MIME type
            mime_type = FileValidator.get_mime_type(video_file.filename)
            
            # Analyze video using interview evaluator
            evaluator = InterviewEvaluator()
            analysis_result = evaluator.evaluate(video_bytes, mime_type)
            
            # Parse evaluation data
            evaluation_data = ResponseParser.parse_evaluation_response(analysis_result)
            
            # Calculate overall score
            total_score = sum(int(item['score'].split('/')[0]) for item in evaluation_data)
            overall_score = f"{total_score}/100"
            
            return jsonify({
                'success': True,
                'filename': secure_filename(video_file.filename),
                'overall_score': overall_score,
                'evaluations': evaluation_data,
                'summary': {
                    'total_metrics': len(evaluation_data),
                    'average_score': f"{total_score/10:.1f}/10"
                }
            }), 200
            
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': f"Evaluation parsing error: {str(e)}"
            }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @staticmethod
    def analyze_video(request):
        """Handle general video analysis requests"""
        try:
            # Validate request has video file
            if 'video' not in request.files:
                return jsonify({'error': 'No video file provided'}), 400
            
            video_file = request.files['video']
            
            # Validate file
            validation_error = FileValidator.validate_video_file(video_file)
            if validation_error:
                return validation_error
            
            # Get prompt (optional)
            prompt = request.form.get('prompt', 'Please summarize the video in 3 sentences.')
            
            # Read video bytes
            video_bytes = video_file.read()
            
            # Check file size
            if len(video_bytes) > 100 * 1024 * 1024:  # 100MB
                return jsonify({'error': 'File size exceeds 100MB limit'}), 400
            
            # Get MIME type
            mime_type = FileValidator.get_mime_type(video_file.filename)
            
            # Analyze video
            analyzer = VideoAnalyzer()
            analysis_result = analyzer.analyze(video_bytes, mime_type, prompt)
            
            return jsonify({
                'success': True,
                'filename': secure_filename(video_file.filename),
                'analysis': analysis_result,
                'prompt': prompt
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500