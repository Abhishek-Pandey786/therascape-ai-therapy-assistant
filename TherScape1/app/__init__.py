from flask import Flask
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    from config import config
    config_name = os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config.get(config_name, config['default']))
    
    # Enable CORS for microservices communication
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Set secret key for sessions
    app.secret_key = app.config['SECRET_KEY']
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    return app 