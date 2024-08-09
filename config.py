import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.environ.get('GOOGLE_API_KEY')
    QDRANT_URL = os.environ.get('QDRANT_URL')
    QDRANT_API_KEY = os.environ.get('QDRANT_API_KEY')
    NEO4J_URI = os.environ.get('NEO4J_URI')
    NEO4J_USERNAME = os.environ.get('NEO4J_USERNAME')
    NEO4J_PASSWORD = os.environ.get('NEO4J_PASSWORD')
    CORS_HEADERS = 'Content-Type'
    DEBUG = False
    TESTING = False
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/app/uploads')
    ELDERS_DATA_DIR = os.environ.get('ELDERS_DATA_DIR', '/app/elders_data')
    DATABASE_PATH = os.getenv('DATABASE_PATH', "/app/database/residents.db")

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    pass

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    config_name = os.environ.get('FLASK_CONFIG', 'default')
    return config[config_name]