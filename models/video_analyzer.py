import google.generativeai as genai
from config.settings import Config

class VideoAnalyzer:
    """Model for general video analysis using Gemini API"""
    
    def __init__(self):
        # Configure Gemini API
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def analyze(self, video_bytes, mime_type, prompt):
        """
        Analyze video with custom prompt
        
        Args:
            video_bytes: Binary video data
            mime_type: MIME type of the video
            prompt: Custom analysis prompt
            
        Returns:
            str: Analysis result from Gemini
        """
        try:
            # Create content with video and text prompt
            response = self.model.generate_content([
                {
                    "mime_type": mime_type,
                    "data": video_bytes
                },
                prompt
            ])
            
            return response.text
            
        except Exception as e:
            raise Exception(f"Error analyzing video: {str(e)}")