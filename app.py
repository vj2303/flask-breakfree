from flask import Flask, request
from config.settings import Config
from routes import video_bp, health_bp, profile_bp
from utils.error_handlers import register_error_handlers
from utils.mongo_logger import MongoLogger
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Load configuration
    app.config.from_object(Config)
    
    # Register blueprints
    app.register_blueprint(video_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(profile_bp)
    
    # Register error handlers
    register_error_handlers(app)

    mongo_logger = MongoLogger()

    @app.after_request
    def log_response(response):
        try:
            response_body = response.get_data(as_text=True)
        except Exception:
            response_body = '<unable to decode>'
        mongo_logger.log_response(
            endpoint=request.path,
            method=request.method,
            status_code=response.status_code,
            response_body=response_body
        )
        return response

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)