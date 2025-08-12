import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # File upload configuration
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max file size
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}
    
    # Gemini API configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyDqkgoA43NZbSBn7bLrQjb7g9vpZoY8gVg')
    
    # MIME type mappings
    MIME_TYPES = {
        'mp4': 'video/mp4',
        'avi': 'video/x-msvideo',
        'mov': 'video/quicktime',
        'mkv': 'video/x-matroska',
        'webm': 'video/webm'
    }