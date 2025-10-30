# Video recommendation service to communicate with Java backend
import requests
import os
from flask import session
from typing import List, Dict, Optional

class VideoService:
    def __init__(self):
        self.java_backend_url = os.getenv('JAVA_BACKEND_URL', 'http://localhost:8080')
        self.api_base = f"{self.java_backend_url}/api"
    
    def get_videos_by_mood(self, mood_category: str) -> List[Dict]:
        """Get video recommendations based on mood from Java backend"""
        try:
            token = session.get('jwt_token')
            headers = {}
            if token:
                headers['Authorization'] = f'Bearer {token}'
            
            response = requests.get(
                f"{self.api_base}/videos/mood/{mood_category.lower()}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                videos = response.json()
                return videos if isinstance(videos, list) else []
            
            return []
        except requests.RequestException as e:
            print(f"Error fetching videos: {e}")
            return []
    
    def get_recommended_videos_for_emotion(self, emotion: str) -> List[Dict]:
        """Map emotion to mood category and get videos"""
        # Map emotions to mood categories
        emotion_to_mood_mapping = {
            'happy': 'happy',
            'sad': 'sad',
            'anxious': 'anxious',
            'angry': 'angry',
            'stressed': 'stressed',
            'depressed': 'depressed',
            'neutral': 'neutral',
            'frustrated': 'angry',
            'lonely': 'sad',
            'overwhelmed': 'stressed'
        }
        
        mood_category = emotion_to_mood_mapping.get(emotion.lower(), 'neutral')
        return self.get_videos_by_mood(mood_category)
    
    def format_videos_for_frontend(self, videos: List[Dict]) -> List[Dict]:
        """Format video data for frontend consumption"""
        formatted_videos = []
        
        for video in videos:
            formatted_video = {
                'id': video.get('id'),
                'title': video.get('title'),
                'description': video.get('description'),
                'videoUrl': video.get('videoUrl'),
                'moodCategory': video.get('moodCategory'),
                'thumbnail': self._generate_thumbnail_url(video.get('videoUrl')),
                'duration': self._extract_duration(video.get('videoUrl'))
            }
            formatted_videos.append(formatted_video)
        
        return formatted_videos
    
    def _generate_thumbnail_url(self, video_url: str) -> str:
        """Generate thumbnail URL for YouTube videos"""
        if 'youtu.be' in video_url or 'youtube.com' in video_url:
            # Extract video ID and generate thumbnail
            video_id = self._extract_youtube_id(video_url)
            if video_id:
                return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        
        return "/static/images/default-video-thumbnail.jpg"
    
    def _extract_youtube_id(self, url: str) -> Optional[str]:
        """Extract YouTube video ID from URL"""
        import re
        
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/)([^&\n?#]+)',
            r'youtube\.com/embed/([^&\n?#]+)',
            r'youtube\.com/v/([^&\n?#]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_duration(self, video_url: str) -> str:
        """Extract or estimate video duration"""
        # This could be enhanced with YouTube API integration
        return "Unknown"

# Create global instance
video_service = VideoService()
