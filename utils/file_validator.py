from flask import jsonify
from config.settings import Config

class FileValidator:
    """Utility class for file validation operations"""
    
    @staticmethod
    def allowed_file(filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
    
    @staticmethod
    def get_mime_type(filename):
        """Get MIME type based on file extension"""
        extension = filename.rsplit('.', 1)[1].lower()
        return Config.MIME_TYPES.get(extension, 'video/mp4')
    
    @staticmethod
    def validate_video_file(video_file):
        """
        Validate video file for upload
        
        Args:
            video_file: FileStorage object from Flask request
            
        Returns:
            dict or None: Error response if validation fails, None if valid
        """
        # Check if file is selected
        if video_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if file type is allowed
        if not FileValidator.allowed_file(video_file.filename):
            return jsonify({
                'error': f'File type not allowed. Supported formats: {", ".join(Config.ALLOWED_EXTENSIONS)}'
            }), 400
        
        return None