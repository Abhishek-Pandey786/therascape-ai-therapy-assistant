# Authentication service to communicate with Java backend
import requests
import os
from flask import session
from typing import Dict, Optional

class AuthService:
    def __init__(self):
        self.java_backend_url = os.getenv('JAVA_BACKEND_URL', 'http://localhost:8080')
        self.api_base = f"{self.java_backend_url}/api"
    
    def register_user(self, registration_data: Dict) -> Dict:
        """Register a new user via Java backend"""
        try:
            response = requests.post(
                f"{self.api_base}/auth/register",
                json=registration_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 201:
                return {
                    'success': True,
                    'user': response.json(),
                    'message': 'Registration successful'
                }
            else:
                return {
                    'success': False,
                    'message': response.text or 'Registration failed'
                }
        except requests.RequestException as e:
            return {
                'success': False,
                'message': f'Connection error: {str(e)}'
            }
    
    def login_user(self, login_data: Dict) -> Dict:
        """Login user via Java backend"""
        try:
            response = requests.post(
                f"{self.api_base}/auth/login",
                json=login_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    # Store JWT token in session
                    session['jwt_token'] = data.get('token')
                    session['user_data'] = data.get('user')
                    return {
                        'success': True,
                        'user': data.get('user'),
                        'token': data.get('token'),
                        'message': 'Login successful'
                    }
            
            return {
                'success': False,
                'message': response.json().get('message', 'Login failed')
            }
        except requests.RequestException as e:
            return {
                'success': False,
                'message': f'Connection error: {str(e)}'
            }
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user details from Java backend"""
        try:
            token = session.get('jwt_token')
            if not token:
                return None
            
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.api_base}/users/username/{username}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except requests.RequestException:
            return None
    
    def check_username_exists(self, username: str) -> bool:
        """Check if username exists"""
        try:
            response = requests.get(
                f"{self.api_base}/auth/check-username/{username}",
                timeout=10
            )
            return response.status_code == 200 and response.json()
        except requests.RequestException:
            return False
    
    def check_email_exists(self, email: str) -> bool:
        """Check if email exists"""
        try:
            response = requests.get(
                f"{self.api_base}/auth/check-email/{email}",
                timeout=10
            )
            return response.status_code == 200 and response.json()
        except requests.RequestException:
            return False
    
    def validate_token(self) -> bool:
        """Validate current JWT token"""
        token = session.get('jwt_token')
        if not token:
            return False
        
        try:
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get(
                f"{self.api_base}/users/me",  # You might need to add this endpoint
                headers=headers,
                timeout=10
            )
            return response.status_code == 200
        except requests.RequestException:
            return False
    
    def logout_user(self):
        """Clear session data completely"""
        # Clear all session data
        session.clear()
        
        # Force session to be deleted on next request
        session.permanent = False

# Create global instance
auth_service = AuthService()
