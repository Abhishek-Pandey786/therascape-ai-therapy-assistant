#!/usr/bin/env python3
"""
Integration Test Suite for TheraScape Java Backend Integration

This script tests the integration between the Python Flask frontend
and the Java Spring Boot backend.

Usage:
    python test_integration.py
"""

import requests
import json
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class IntegrationTester:
    def __init__(self):
        self.flask_url = "http://localhost:5000"
        self.java_url = os.getenv('JAVA_BACKEND_URL', 'http://localhost:8080')
        self.test_user = {
            "username": "testuser123",
            "password": "testpass123",
            "email": "test@example.com",
            "fullName": "Test User"
        }
        
    def print_status(self, test_name, status, message=""):
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {test_name}: {message}")
        
    def test_backend_connectivity(self):
        """Test if both backends are running"""
        print("\n🔌 Testing Backend Connectivity...")
        
        # Test Flask backend
        try:
            response = requests.get(f"{self.flask_url}/", timeout=5)
            flask_status = response.status_code == 200
            self.print_status("Flask Backend", flask_status, f"Status: {response.status_code}")
        except Exception as e:
            self.print_status("Flask Backend", False, f"Error: {str(e)}")
            flask_status = False
            
        # Test Java backend
        try:
            response = requests.get(f"{self.java_url}/api/users/1", timeout=5)
            java_status = response.status_code in [200, 404]  # 404 is OK, means backend is running
            self.print_status("Java Backend", java_status, f"Status: {response.status_code}")
        except Exception as e:
            self.print_status("Java Backend", False, f"Error: {str(e)}")
            java_status = False
            
        return flask_status and java_status
    
    def test_user_registration(self):
        """Test user registration through Flask proxy"""
        print("\n👤 Testing User Registration...")
        
        try:
            response = requests.post(
                f"{self.flask_url}/api/register",
                json=self.test_user,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            success = response.status_code in [200, 201, 409]  # 409 = user already exists
            
            if response.status_code == 409:
                self.print_status("User Registration", True, "User already exists (expected)")
            elif success:
                self.print_status("User Registration", True, f"Status: {response.status_code}")
            else:
                self.print_status("User Registration", False, f"Status: {response.status_code}, Response: {response.text}")
                
            return success
            
        except Exception as e:
            self.print_status("User Registration", False, f"Error: {str(e)}")
            return False
    
    def test_user_login(self):
        """Test user login through Flask proxy"""
        print("\n🔐 Testing User Login...")
        
        try:
            login_data = {
                "username": self.test_user["username"],
                "password": self.test_user["password"]
            }
            
            response = requests.post(
                f"{self.flask_url}/api/login",
                json=login_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            success = response.status_code == 200
            
            if success:
                response_data = response.json()
                has_token = 'token' in response_data
                self.print_status("User Login", success, f"Token received: {has_token}")
                return response_data.get('token') if has_token else None
            else:
                self.print_status("User Login", False, f"Status: {response.status_code}, Response: {response.text}")
                return None
                
        except Exception as e:
            self.print_status("User Login", False, f"Error: {str(e)}")
            return None
    
    def test_video_recommendations(self):
        """Test video recommendations API"""
        print("\n🎥 Testing Video Recommendations...")
        
        moods = ['happy', 'sad', 'anxious', 'angry', 'calm']
        
        for mood in moods:
            try:
                response = requests.get(
                    f"{self.flask_url}/api/videos/mood/{mood}",
                    timeout=10
                )
                
                success = response.status_code == 200
                
                if success:
                    videos = response.json()
                    video_count = len(videos) if isinstance(videos, list) else 0
                    self.print_status(f"Videos for {mood}", True, f"Found {video_count} videos")
                else:
                    self.print_status(f"Videos for {mood}", False, f"Status: {response.status_code}")
                    
            except Exception as e:
                self.print_status(f"Videos for {mood}", False, f"Error: {str(e)}")
    
    def test_chat_integration(self):
        """Test chat with video recommendations"""
        print("\n💬 Testing Chat Integration...")
        
        try:
            # Create a session first
            session = requests.Session()
            
            # Login to get authenticated session
            login_data = {
                "username": self.test_user["username"],
                "password": self.test_user["password"]
            }
            
            login_response = session.post(
                f"{self.flask_url}/api/login",
                json=login_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if login_response.status_code == 200:
                # Send a chat message
                chat_data = {"message": "I'm feeling really sad today"}
                
                chat_response = session.post(
                    f"{self.flask_url}/chat",
                    json=chat_data,
                    headers={'Content-Type': 'application/json'},
                    timeout=15
                )
                
                success = chat_response.status_code == 200
                
                if success:
                    response_data = chat_response.json()
                    has_response = 'response' in response_data
                    has_videos = 'videos' in response_data
                    self.print_status("Chat Integration", True, f"Response: {has_response}, Videos: {has_videos}")
                else:
                    self.print_status("Chat Integration", False, f"Status: {chat_response.status_code}")
            else:
                self.print_status("Chat Integration", False, "Could not authenticate for chat test")
                
        except Exception as e:
            self.print_status("Chat Integration", False, f"Error: {str(e)}")
    
    def run_all_tests(self):
        """Run the complete integration test suite"""
        print("🧪 TheraScape Integration Test Suite")
        print("=" * 50)
        
        # Test 1: Backend connectivity
        if not self.test_backend_connectivity():
            print("\n❌ Backend connectivity failed. Please ensure both backends are running:")
            print(f"   - Flask: {self.flask_url}")
            print(f"   - Java: {self.java_url}")
            return
        
        # Test 2: User registration
        self.test_user_registration()
        
        # Test 3: User login
        token = self.test_user_login()
        
        # Test 4: Video recommendations
        self.test_video_recommendations()
        
        # Test 5: Chat integration
        self.test_chat_integration()
        
        print("\n" + "=" * 50)
        print("🎉 Integration test suite completed!")
        print("\n📝 Next steps:")
        print("   1. Start your Java backend: mvn spring-boot:run")
        print("   2. Start your Flask frontend: python run.py")
        print("   3. Visit http://localhost:5000 to try the integrated application")


if __name__ == "__main__":
    tester = IntegrationTester()
    tester.run_all_tests()
