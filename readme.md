# Interview Evaluation API - Project Structure

## Directory Structure
```
interview-evaluation-api/
│
├── 📁 config/
│   ├── __init__.py
│   └── settings.py                 # Configuration settings and environment variables
│
├── 📁 controllers/
│   ├── __init__.py
│   └── video_controller.py         # Business logic for video processing endpoints
│
├── 📁 models/
│   ├── __init__.py
│   ├── video_analyzer.py           # General video analysis model
│   └── interview_evaluator.py     # Structured interview evaluation model
│
├── 📁 routes/
│   ├── __init__.py
│   ├── video_routes.py             # Video-related API endpoints
│   └── health_routes.py            # Health check endpoints
│
├── 📁 utils/
│   ├── __init__.py
│   ├── file_validator.py           # File validation utilities
│   ├── response_parser.py          # AI response parsing utilities
│   └── error_handlers.py           # Flask error handlers
│
├── app.py                          # Main application entry point
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
└── README.md                       # Project documentation
```

## File Descriptions

### Core Application Files
- **app.py**: Main Flask application factory and entry point
- **requirements.txt**: All Python package dependencies

### Configuration
- **config/settings.py**: Centralized configuration management including API keys, file size limits, and allowed extensions

### Routes (API Endpoints)
- **routes/video_routes.py**: Endpoints for `/evaluate-interview` and `/analyze-video`
- **routes/health_routes.py**: Health check endpoint `/health`

### Controllers (Business Logic)
- **controllers/video_controller.py**: Contains the main business logic for processing video analysis requests

### Models (Data Processing)
- **models/video_analyzer.py**: Handles general video analysis using Gemini API
- **models/interview_evaluator.py**: Specialized model for structured interview evaluation

### Utils (Helper Functions)
- **utils/file_validator.py**: File validation, MIME type detection, and upload validation
- **utils/response_parser.py**: Parsing and validation of AI-generated responses
- **utils/error_handlers.py**: Centralized error handling for the Flask application

## Key Features Organized
- ✅ **Separation of Concerns**: Each component has a specific responsibility
- ✅ **Modular Design**: Easy to test and maintain individual components
- ✅ **Configuration Management**: Centralized settings and environment variables
- ✅ **Error Handling**: Comprehensive error responses
- ✅ **Code Reusability**: Shared utilities and models

## How to Set Up
1. Create the directory structure as shown above
2. Add `__init__.py` files to make directories Python packages
3. Copy each file content to its respective location
4. Create a `.env` file based on `.env.example`
5. Install dependencies: `pip install -r requirements.txt`
6. Run the application: `python app.py`

### Environment

Create a `.env` file using the template below:

```
GEMINI_API_KEY=your_real_gemini_api_key

## Gemini Profile Manager (New)

Endpoints:

- GET `/` – API info and endpoints list
- GET `/models` – Available Gemini models
- GET `/profiles` – List all profiles
- POST `/profiles` – Create a new profile
- GET `/profiles/<id>` – Get a specific profile
- PUT `/profiles/<id>` – Update a profile
- DELETE `/profiles/<id>` – Delete a profile
- POST `/chat` – Chat using a specific profile
- POST `/chat/stream` – Stream chat using a specific profile

Example `POST /profiles` body:

```json
{
  "title": "Creative Writer",
  "system_instruction": "You are a creative writing assistant...",
  "model": "gemini-1.5-pro",
  "temperature": 0.7,
  "top_k": 40,
  "top_p": 0.9,
  "max_output_tokens": 2048
}
```
```

## API Endpoints
- **POST** `/evaluate-interview` - Structured interview evaluation
- **POST** `/analyze-video` - General video analysis with custom prompts  
- **GET** `/health` - Health check endpoint