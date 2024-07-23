from flask import Flask
from flask_cors import CORS
from config import get_config
from app.utils.gemini_initializer import GeminiInitializer

def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    
    CORS(app)

    # Initialize Gemini
    app.gemini = GeminiInitializer()

    # Register blueprints
    from app.routes import care_note_bp, care_plan_bp, care_story_bp, care_plan_spilt_bp, file_upload_bp, add_elder_bp
    app.register_blueprint(care_note_bp)
    app.register_blueprint(care_plan_bp)
    app.register_blueprint(care_story_bp)
    app.register_blueprint(care_plan_spilt_bp)
    app.register_blueprint(file_upload_bp)
    app.register_blueprint(add_elder_bp)


    return app