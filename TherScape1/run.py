from app import create_app
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check for API key
api_key = os.getenv('GOOGLE_API_KEY')
if api_key and api_key != 'your_google_api_key_here':
    print(f"✅ Google API key loaded: {api_key[:10]}...")
else:
    print("⚠️  WARNING: GOOGLE_API_KEY not set or using default value.")
    print("Please set your Gemini API key in the .env file.")
    print("The application will run but AI features will be limited.")

app = create_app()

# Set a secret key for session encryption
app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key-for-development')

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'true').lower() == 'true'
    port = int(os.getenv('FLASK_PORT', 5000))
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    
    print(f"\n🚀 Starting TheraScape on {host}:{port}")
    print(f"🔧 Debug mode: {debug_mode}")
    print(f"🔗 Java Backend: {os.getenv('JAVA_BACKEND_URL', 'Not configured')}")
    print(f"🎯 Features enabled:")
    print(f"   - User Authentication: {os.getenv('ENABLE_USER_AUTHENTICATION', 'false')}")
    print(f"   - Video Recommendations: {os.getenv('ENABLE_VIDEO_RECOMMENDATIONS', 'false')}")
    print(f"   - Java Backend Integration: {os.getenv('ENABLE_JAVA_BACKEND', 'false')}")
    print("=" * 50)
    
    app.run(debug=debug_mode, host=host, port=port) 