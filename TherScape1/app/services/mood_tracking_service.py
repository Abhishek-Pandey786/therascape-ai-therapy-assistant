# Enhanced mood tracking service to communicate with Java backend
import requests
import os
from flask import session
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class MoodTrackingService:
    def __init__(self):
        self.java_backend_url = os.getenv('JAVA_BACKEND_URL', 'http://localhost:8080')
        self.api_base = f"{self.java_backend_url}/api"
    
    def store_mood_analysis(self, text: str, mood_data: Dict, user_id: Optional[int] = None) -> Dict:
        """Store mood analysis data in Java backend"""
        try:
            token = session.get('jwt_token')
            headers = {'Content-Type': 'application/json'}
            if token:
                headers['Authorization'] = f'Bearer {token}'
            
            request_data = {
                'text': text,
                'intensity': mood_data.get('intensity', 5),
                'preferences': mood_data.get('preferences', {}),
                'userId': user_id or session.get('user_data', {}).get('id'),
                'sessionId': session.get('session_id')
            }
            
            response = requests.post(
                f"{self.api_base}/mood/analyze",
                json=request_data,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'analysis': response.json(),
                    'message': 'Mood analysis stored successfully'
                }
            else:
                return {
                    'success': False,
                    'message': f'Failed to store mood analysis: {response.status_code}'
                }
        except requests.RequestException as e:
            return {
                'success': False,
                'message': f'Connection error: {str(e)}'
            }
    
    def get_user_mood_history(self, user_id: Optional[int] = None, days: int = 7) -> List[Dict]:
        """Get user's mood history from Java backend"""
        try:
            token = session.get('jwt_token')
            if not token:
                return []
            
            target_user_id = user_id or session.get('user_data', {}).get('id')
            if not target_user_id:
                return []
            
            headers = {'Authorization': f'Bearer {token}'}
            
            response = requests.get(
                f"{self.api_base}/mood/history/{target_user_id}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            return []
        except requests.RequestException:
            return []
    
    def get_user_mood_trends(self, user_id: Optional[int] = None) -> Dict:
        """Get user's mood trends and analytics from Java backend"""
        try:
            token = session.get('jwt_token')
            if not token:
                return {}
            
            target_user_id = user_id or session.get('user_data', {}).get('id')
            if not target_user_id:
                return {}
            
            headers = {'Authorization': f'Bearer {token}'}
            
            response = requests.get(
                f"{self.api_base}/mood/trends/{target_user_id}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            return {}
        except requests.RequestException:
            return {}
    
    def format_mood_history_for_chart(self, mood_history: List[Dict]) -> Dict:
        """Format mood history data for frontend charts"""
        if not mood_history:
            return {
                'labels': [],
                'datasets': [{
                    'label': 'Mood Intensity',
                    'data': [],
                    'borderColor': 'rgb(75, 192, 192)',
                    'backgroundColor': 'rgba(75, 192, 192, 0.2)'
                }]
            }
        
        # Sort by date
        sorted_history = sorted(mood_history, key=lambda x: x.get('date', ''))
        
        labels = []
        intensity_data = []
        mood_colors = {
            'happy': '#4CAF50',
            'calm': '#2196F3',
            'neutral': '#9E9E9E',
            'anxious': '#FF9800',
            'sad': '#607D8B',
            'angry': '#F44336',
            'stressed': '#795548'
        }
        
        for entry in sorted_history[-7:]:  # Last 7 entries
            date_str = entry.get('date', '')
            if isinstance(date_str, str):
                try:
                    date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    labels.append(date_obj.strftime('%m/%d'))
                except:
                    labels.append(date_str)
            else:
                labels.append(str(date_str))
            
            intensity_data.append(entry.get('intensity', 5))
        
        return {
            'labels': labels,
            'datasets': [{
                'label': 'Mood Intensity',
                'data': intensity_data,
                'borderColor': 'rgb(75, 192, 192)',
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'tension': 0.1
            }]
        }
    
    def format_mood_trends_for_dashboard(self, trends: Dict) -> Dict:
        """Format mood trends for dashboard display"""
        if not trends:
            return {
                'averageIntensity': 'N/A',
                'mostCommonMood': 'N/A',
                'improvementTrend': 'N/A',
                'weeklyAverage': 'N/A',
                'moodDistribution': {}
            }
        
        # Format numbers
        avg_intensity = trends.get('averageIntensity')
        if isinstance(avg_intensity, (int, float)):
            trends['averageIntensity'] = round(avg_intensity, 1)
        
        weekly_avg = trends.get('weeklyAverage')
        if isinstance(weekly_avg, (int, float)):
            trends['weeklyAverage'] = round(weekly_avg, 1)
        
        return trends
    
    def detect_concerning_patterns(self, mood_history: List[Dict], trends: Dict) -> List[str]:
        """Detect concerning patterns in mood data"""
        concerns = []
        
        if not mood_history or not trends:
            return concerns
        
        # Check for consistently low mood
        recent_entries = mood_history[-5:] if len(mood_history) >= 5 else mood_history
        low_mood_count = sum(1 for entry in recent_entries if entry.get('intensity', 5) <= 3)
        
        if low_mood_count >= 3:
            concerns.append("Consistently low mood detected in recent entries")
        
        # Check for crisis indicators
        crisis_moods = ['depressed', 'hopeless', 'suicidal']
        recent_moods = [entry.get('mood', '').lower() for entry in recent_entries]
        
        if any(mood in crisis_moods for mood in recent_moods):
            concerns.append("Crisis-related mood patterns detected")
        
        # Check for declining trend
        avg_intensity = trends.get('averageIntensity', 5)
        if isinstance(avg_intensity, (int, float)) and avg_intensity < 4:
            concerns.append("Below-average mood intensity over time")
        
        return concerns

# Create global instance
mood_tracking_service = MoodTrackingService()
