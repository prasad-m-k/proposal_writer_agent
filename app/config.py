import os
from pathlib import Path

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Determine if we're running in Docker or locally
    if os.path.exists('/.dockerenv'):
        # Running in Docker container
        BASE_DIR = '/app'
    else:
        # Running locally
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        BASE_DIR = os.path.join(BASE_DIR, '..')  # Go up one level to project root
    
    INPUT_FILES_FOLDER = os.environ.get('INPUT_FILES_FOLDER', os.path.join(BASE_DIR, 'uploads'))
    OUTPUT_FILES_FOLDER = os.environ.get('OUTPUT_FILES_FOLDER', os.path.join(BASE_DIR, 'output'))
    LOG_FOLDER = os.environ.get('LOG_FOLDER', os.path.join(BASE_DIR, 'logs'))
    
    # Ensure directories exist
    for folder in [INPUT_FILES_FOLDER, OUTPUT_FILES_FOLDER, LOG_FOLDER]:
        Path(folder).mkdir(parents=True, exist_ok=True)

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    DEBUG = False
    FLASK_ENV = 'production'
