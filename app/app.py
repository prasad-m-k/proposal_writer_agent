"""
Main Flask Application - Modular Version
"""
import os
from flask import Flask
from dotenv import load_dotenv

from config.settings import config_map
from routes.main_routes import main_bp, init_services


def create_app(config_name=None):
    """Application factory function"""
    app = Flask(__name__)
    
    # Load environment variables
    load_dotenv()
    
    # Determine configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
    
    # Configure app
    config_class = config_map.get(config_name, config_map['default'])
    config_instance = config_class()
    config_instance.init_app(app)
    
    # Configure Gemini AI
    _configure_genai(app)
    
    # Set up security headers
    _setup_security_headers(app)
    
    # Initialize services
    init_services(app)
    
    # Register blueprints
    app.register_blueprint(main_bp)
    
    return app


def _configure_genai(app):
    """Configure Google Generative AI"""
    import google.generativeai as genai
    
    api_key = app.config.get('GEMINI_API_KEY')
    if api_key:
        genai.configure(api_key=api_key)
    else:
        print("Warning: GEMINI_API_KEY not configured")


def _setup_security_headers(app):
    """Set up security headers for all responses"""
    
    @app.after_request
    def apply_security_headers(response):
        """Apply security-enhancing HTTP headers to every response"""
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com data:; "
        )
        response.headers['Content-Security-Policy'] = csp
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        if app.config.get('DEPL') == "PROD":
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response


# Create the application instance
app = create_app()

if __name__ == '__main__':
    # Development server
    debug_mode = os.getenv('FLASK_ENV', 'development') == 'development'
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5001)),
        debug=debug_mode
    )
