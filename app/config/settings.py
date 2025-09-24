"""
Application Configuration Module
"""
import os
from pathlib import Path

class Config:
    """Base configuration class"""
    SECRET_KEY = os.getenv("SECRET_KEY", "a_super_secret_key_for_dev_if_not_set")
    
    # Folder configurations
    INPUT_FILES_FOLDER_NAME = 'input_data'
    DOWNLOAD_FOLDER_NAME = 'generated_proposals'
    
    def __init__(self, app=None):
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize app configuration"""
        app.config['SECRET_KEY'] = self.SECRET_KEY
        
        # Set up paths
        app.config['INPUT_FILES_FOLDER'] = os.path.abspath(self.INPUT_FILES_FOLDER_NAME)
        app.config['DOWNLOAD_FOLDER'] = os.path.abspath(self.DOWNLOAD_FOLDER_NAME)
        
        # Create directories if they don't exist
        self._create_directories(app)
        
        # Load environment variables
        self._load_env_vars(app)
    
    def _create_directories(self, app):
        """Create necessary directories"""
        for folder in [app.config['INPUT_FILES_FOLDER'], app.config['DOWNLOAD_FOLDER']]:
            if not os.path.exists(folder):
                os.makedirs(folder)
    
    def _load_env_vars(self, app):
        """Load required environment variables"""
        required_vars = ["GEMINI_API_KEY", "GEMINI_API_KEY_ALTERNATE"]
        
        for var in required_vars:
            value = os.getenv(var)
            if not value:
                raise ValueError(f"{var} not set. Please set it in your .env file.")
            app.config[var] = value
        
        app.config['DEPL'] = os.getenv("DEPL", "DEV")

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'

# Configuration mapping
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# RFP Type to file mapping
RFP_TYPE_FILES = {
    "Extended Learning Opportunities Program": {
        "prompt": "proposal_prompt.txt",
        "requirements": "natomas_school_district_rfp_requirements.txt"
    },
    "Request for Qualifications": {
        "yaml": "natomas_school_district_rfp1.yaml",
        "jinja": "natomas_school_district_jinja1.md"
    },
    "Summer School Core Program Providers": {
        "yaml": "natomas_school_district_rfp2.yaml",
        "jinja": "natomas_school_district_jinja2.md"
    },
    "After School Core Program Providers": {
        "yaml": "natomas_school_district_rfp3.yaml",
        "jinja": "natomas_school_district_jinja3.md"
    }
}
