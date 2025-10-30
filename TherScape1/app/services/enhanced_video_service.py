# Enhanced Video Service for Mood-Based Recommendations
import requests
import os
from flask import session
from typing import List, Dict, Optional
from app.models.mood_scene_mapping import MoodAnalysisResult

class EnhancedVideoService:
    def __init__(self):
        self.java_backend_url = os.getenv('JAVA_BACKEND_URL', 'http://localhost:8080')
        self.api_base = f"{self.java_backend_url}/api"
    
    def get_personalized_video_recommendations(self, 
                                              username: str, 
                                              mood_analysis: MoodAnalysisResult,
                                              max_duration: int = 30) -> List[Dict]:
        """Get personalized video recommendations based on comprehensive mood analysis"""
        try:
            token = session.get('jwt_token')
            headers = {}
            if token:
                headers['Authorization'] = f'Bearer {token}'
            
            params = {
                'moodCategory': mood_analysis.primary_mood.value,
                'moodIntensity': mood_analysis.intensity,
                'crisisRisk': mood_analysis.crisis_risk,
                'maxDuration': max_duration
            }
            
            response = requests.get(
                f"{self.api_base}/enhanced-videos/personalized/{username}",
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                videos = response.json()
                return self.format_videos_for_frontend(videos)
            
            return []
        except requests.RequestException as e:
            print(f"Error fetching personalized videos: {e}")
            return []
    
    def get_quick_help_videos(self, mood_category: str) -> List[Dict]:
        """Get quick help videos for immediate intervention"""
        try:
            token = session.get('jwt_token')
            headers = {}
            if token:
                headers['Authorization'] = f'Bearer {token}'
            
            response = requests.get(
                f"{self.api_base}/enhanced-videos/quick-help/{mood_category.lower()}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                videos = response.json()
                return self.format_videos_for_frontend(videos)
            
            return []
        except requests.RequestException as e:
            print(f"Error fetching quick help videos: {e}")
            return []
    
    def get_beginner_videos(self, mood_category: str) -> List[Dict]:
        """Get beginner-friendly videos for new users"""
        try:
            token = session.get('jwt_token')
            headers = {}
            if token:
                headers['Authorization'] = f'Bearer {token}'
            
            response = requests.get(
                f"{self.api_base}/enhanced-videos/beginner/{mood_category.lower()}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                videos = response.json()
                return self.format_videos_for_frontend(videos)
            
            return []
        except requests.RequestException as e:
            print(f"Error fetching beginner videos: {e}")
            return []
    
    def get_videos_by_therapeutic_goals(self, goals: List[str]) -> List[Dict]:
        """Get videos that match specific therapeutic goals"""
        try:
            token = session.get('jwt_token')
            headers = {}
            if token:
                headers['Authorization'] = f'Bearer {token}'
            
            params = {'goals': goals}
            
            response = requests.get(
                f"{self.api_base}/enhanced-videos/therapeutic-goals",
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                videos = response.json()
                return self.format_videos_for_frontend(videos)
            
            return []
        except requests.RequestException as e:
            print(f"Error fetching therapeutic goal videos: {e}")
            return []
    
    def get_videos_by_content_type(self, content_type: str, mood_category: str) -> List[Dict]:
        """Get videos by content type (meditation, breathing, therapy, etc.)"""
        try:
            token = session.get('jwt_token')
            headers = {}
            if token:
                headers['Authorization'] = f'Bearer {token}'
            
            params = {'moodCategory': mood_category.lower()}
            
            response = requests.get(
                f"{self.api_base}/enhanced-videos/content-type/{content_type.lower()}",
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                videos = response.json()
                return self.format_videos_for_frontend(videos)
            
            return []
        except requests.RequestException as e:
            print(f"Error fetching content type videos: {e}")
            return []
    
    def get_videos_by_scenario(self, scenario_type: str, mood_category: str) -> List[Dict]:
        """Get videos by scenario type (nature, beach, forest, etc.)"""
        try:
            token = session.get('jwt_token')
            headers = {}
            if token:
                headers['Authorization'] = f'Bearer {token}'
            
            params = {'moodCategory': mood_category.lower()}
            
            response = requests.get(
                f"{self.api_base}/enhanced-videos/scenario/{scenario_type.lower()}",
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                videos = response.json()
                return self.format_videos_for_frontend(videos)
            
            return []
        except requests.RequestException as e:
            print(f"Error fetching scenario videos: {e}")
            return []
    
    def get_popular_videos(self, mood_category: str, limit: int = 5) -> List[Dict]:
        """Get popular videos for a specific mood category"""
        try:
            token = session.get('jwt_token')
            headers = {}
            if token:
                headers['Authorization'] = f'Bearer {token}'
            
            params = {'limit': limit}
            
            response = requests.get(
                f"{self.api_base}/enhanced-videos/popular/{mood_category.lower()}",
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                videos = response.json()
                return self.format_videos_for_frontend(videos)
            
            return []
        except requests.RequestException as e:
            print(f"Error fetching popular videos: {e}")
            return []
    
    def record_video_interaction(self, video_id: str, username: str, interaction_type: str):
        """Record user interaction with a video for analytics"""
        try:
            token = session.get('jwt_token')
            headers = {}
            if token:
                headers['Authorization'] = f'Bearer {token}'
            
            params = {
                'videoId': video_id,
                'username': username,
                'interactionType': interaction_type
            }
            
            response = requests.post(
                f"{self.api_base}/enhanced-videos/interaction",
                headers=headers,
                params=params,
                timeout=10
            )
            
            return response.status_code == 200
        except requests.RequestException as e:
            print(f"Error recording video interaction: {e}")
            return False
    
    def format_videos_for_frontend(self, videos: List[Dict]) -> List[Dict]:
        """Format video data for frontend consumption with enhanced features"""
        formatted_videos = []
        
        for video in videos:
            formatted_video = {
                'id': video.get('id'),
                'title': video.get('title'),
                'description': video.get('description'),
                'videoUrl': video.get('videoUrl'),
                'thumbnailUrl': video.get('thumbnailUrl') or self._generate_thumbnail_url(video.get('videoUrl')),
                'duration': video.get('durationMinutes', 0),
                'primaryMoodCategory': video.get('primaryMoodCategory'),
                'secondaryMoodCategories': video.get('secondaryMoodCategories', []),
                'therapyTechnique': video.get('therapyTechnique'),
                'contentType': video.get('contentType'),
                'scenarioType': video.get('scenarioType'),
                'therapeuticGoals': video.get('therapeuticGoals', []),
                'difficultyLevel': video.get('difficultyLevel', 'beginner'),
                'crisisSafe': video.get('crisisSafe', True),
                'averageRating': video.get('averageRating', 0.0),
                'viewCount': video.get('viewCount', 0),
                'completionRate': video.get('completionRate', 0.0),
                'likeCount': video.get('likeCount', 0),
                'interactiveFeatures': video.get('interactiveFeatures', []),
                'hasSubtitles': video.get('hasSubtitles', False),
                'availableLanguages': video.get('availableLanguages', ['English']),
                'moodIntensityMin': video.get('moodIntensityMin', 1),
                'moodIntensityMax': video.get('moodIntensityMax', 10),
                'tags': self._generate_tags(video)
            }
            formatted_videos.append(formatted_video)
        
        return formatted_videos
    
    def _generate_thumbnail_url(self, video_url: str) -> str:
        """Generate thumbnail URL for YouTube videos"""
        if not video_url:
            return "/static/images/default-video-thumbnail.jpg"
            
        if 'youtu.be' in video_url or 'youtube.com' in video_url:
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
    
    def _generate_tags(self, video: Dict) -> List[str]:
        """Generate searchable tags for video"""
        tags = []
        
        # Add mood categories as tags
        if video.get('primaryMoodCategory'):
            tags.append(video['primaryMoodCategory'].lower())
        
        if video.get('secondaryMoodCategories'):
            tags.extend([mood.lower() for mood in video['secondaryMoodCategories']])
        
        # Add therapy technique
        if video.get('therapyTechnique'):
            tags.append(video['therapyTechnique'].lower().replace('_', ' '))
        
        # Add content type
        if video.get('contentType'):
            tags.append(video['contentType'].lower())
        
        # Add scenario type
        if video.get('scenarioType'):
            tags.append(video['scenarioType'].lower().replace('_', ' '))
        
        # Add difficulty level
        if video.get('difficultyLevel'):
            tags.append(video['difficultyLevel'].lower())
        
        # Add duration category
        duration = video.get('durationMinutes', 0)
        if duration <= 5:
            tags.append('quick')
        elif duration <= 15:
            tags.append('short')
        elif duration <= 30:
            tags.append('medium')
        else:
            tags.append('long')
        
        # Add rating category
        rating = video.get('averageRating', 0)
        if rating >= 4.5:
            tags.append('highly rated')
        elif rating >= 4.0:
            tags.append('well rated')
        
        # Add crisis safety
        if video.get('crisisSafe'):
            tags.append('crisis safe')
        
        return list(set(tags))  # Remove duplicates

# Create global instance
enhanced_video_service = EnhancedVideoService()
