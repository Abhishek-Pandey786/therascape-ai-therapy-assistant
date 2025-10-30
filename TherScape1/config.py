# Configuration for integrating with Java Spring Boot backend
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-this'
    
    # Java Backend configuration
    JAVA_BACKEND_URL = os.environ.get('JAVA_BACKEND_URL', 'http://localhost:8080')
    JAVA_BACKEND_TIMEOUT = int(os.environ.get('JAVA_BACKEND_TIMEOUT', '10'))
    
    # Google Gemini API
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    
    # Session configuration
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # CORS configuration for microservices
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:8080', 'http://127.0.0.1:5000']
    
    # Feature flags
    ENABLE_JAVA_BACKEND = os.environ.get('ENABLE_JAVA_BACKEND', 'true').lower() == 'true'
    ENABLE_VIDEO_RECOMMENDATIONS = os.environ.get('ENABLE_VIDEO_RECOMMENDATIONS', 'true').lower() == 'true'
    ENABLE_USER_AUTHENTICATION = os.environ.get('ENABLE_USER_AUTHENTICATION', 'true').lower() == 'true'

class DevelopmentConfig(Config):
    DEBUG = True
    JAVA_BACKEND_URL = 'http://localhost:8080'

class ProductionConfig(Config):
    DEBUG = False
    JAVA_BACKEND_URL = os.environ.get('JAVA_BACKEND_URL', 'https://your-java-backend-url.com')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
