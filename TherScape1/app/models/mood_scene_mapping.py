"""
Mood-to-Scene Mapping System for Java Backend Integration
Standardized mood categories and therapeutic scene recommendations
"""
from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass
import json

class MoodCategory(Enum):
    """Standardized mood categories for consistent backend integration"""
    HAPPY = "happy"
    SAD = "sad"
    ANXIOUS = "anxious"
    ANGRY = "angry"
    STRESSED = "stressed"
    DEPRESSED = "depressed"
    NEUTRAL = "neutral"
    FRUSTRATED = "frustrated"
    LONELY = "lonely"
    OVERWHELMED = "overwhelmed"

class TherapyTechnique(Enum):
    """Therapeutic techniques that can be mapped to AR/VR scenarios"""
    BREATHING_EXERCISES = "breathing_exercises"
    MINDFULNESS_MEDITATION = "mindfulness_meditation"
    PROGRESSIVE_MUSCLE_RELAXATION = "progressive_muscle_relaxation"
    GUIDED_IMAGERY = "guided_imagery"
    GROUNDING_TECHNIQUES = "grounding_techniques"
    COGNITIVE_RESTRUCTURING = "cognitive_restructuring"
    EXPOSURE_THERAPY = "exposure_therapy"
    NATURE_THERAPY = "nature_therapy"
    SOCIAL_INTERACTION = "social_interaction"
    PHYSICAL_ACTIVITY = "physical_activity"

class SceneType(Enum):
    """Types of therapeutic scenes for AR/VR environments"""
    CALMING_NATURE = "calming_nature"
    PEACEFUL_BEACH = "peaceful_beach"
    FOREST_MEDITATION = "forest_meditation"
    MOUNTAIN_RETREAT = "mountain_retreat"
    COZY_INDOOR = "cozy_indoor"
    BREATHING_GARDEN = "breathing_garden"
    SOCIAL_CAFÉ = "social_cafe"
    VIRTUAL_GYM = "virtual_gym"
    ART_THERAPY_STUDIO = "art_therapy_studio"
    CONFIDENCE_STAGE = "confidence_stage"

@dataclass
class SceneRecommendation:
    """Structured scene recommendation for backend integration"""
    scene_type: SceneType
    therapy_technique: TherapyTechnique
    priority: int  # 1-10, higher = more suitable
    description: str
    duration_minutes: int
    interactive_elements: List[str]
    goals: List[str]

@dataclass
class MoodAnalysisResult:
    """Complete mood analysis result for backend integration"""
    primary_mood: MoodCategory
    confidence_score: float  # 0.0-1.0
    secondary_moods: List[MoodCategory]
    intensity: int  # 1-10
    crisis_risk: bool
    scene_recommendations: List[SceneRecommendation]
    therapeutic_goals: List[str]
    session_metadata: Dict

class MoodSceneMapper:
    """Central class for mapping moods to therapeutic scenes"""
    
    def __init__(self):
        self.mood_mappings = self._initialize_mappings()
    
    def _initialize_mappings(self) -> Dict[MoodCategory, List[SceneRecommendation]]:
        """Initialize the mood-to-scene mappings"""
        return {
            MoodCategory.ANXIOUS: [
                SceneRecommendation(
                    scene_type=SceneType.BREATHING_GARDEN,
                    therapy_technique=TherapyTechnique.BREATHING_EXERCISES,
                    priority=10,
                    description="Peaceful garden environment with guided breathing exercises",
                    duration_minutes=10,
                    interactive_elements=["breathing guide", "calming sounds", "visual cues"],
                    goals=["reduce anxiety", "practice breathing", "immediate calming"]
                ),
                SceneRecommendation(
                    scene_type=SceneType.PEACEFUL_BEACH,
                    therapy_technique=TherapyTechnique.GROUNDING_TECHNIQUES,
                    priority=8,
                    description="Beach scene with 5-4-3-2-1 grounding exercise",
                    duration_minutes=15,
                    interactive_elements=["ocean sounds", "tactile feedback", "visual anchors"],
                    goals=["ground in present moment", "reduce overwhelm", "sensory awareness"]
                ),
                SceneRecommendation(
                    scene_type=SceneType.FOREST_MEDITATION,
                    therapy_technique=TherapyTechnique.MINDFULNESS_MEDITATION,
                    priority=7,
                    description="Forest environment for mindfulness practice",
                    duration_minutes=20,
                    interactive_elements=["nature sounds", "guided meditation", "peaceful visuals"],
                    goals=["mindfulness practice", "anxiety reduction", "nature connection"]
                )
            ],
            
            MoodCategory.DEPRESSED: [
                SceneRecommendation(
                    scene_type=SceneType.COZY_INDOOR,
                    therapy_technique=TherapyTechnique.COGNITIVE_RESTRUCTURING,
                    priority=9,
                    description="Warm, safe indoor space for gentle therapy work",
                    duration_minutes=25,
                    interactive_elements=["journal prompts", "thought challenges", "affirmations"],
                    goals=["challenge negative thoughts", "build hope", "self-compassion"]
                ),
                SceneRecommendation(
                    scene_type=SceneType.ART_THERAPY_STUDIO,
                    therapy_technique=TherapyTechnique.GUIDED_IMAGERY,
                    priority=8,
                    description="Creative space for expression and healing",
                    duration_minutes=30,
                    interactive_elements=["art tools", "creative prompts", "self-expression"],
                    goals=["emotional expression", "self-discovery", "mood elevation"]
                ),
                SceneRecommendation(
                    scene_type=SceneType.CALMING_NATURE,
                    therapy_technique=TherapyTechnique.NATURE_THERAPY,
                    priority=7,
                    description="Nature setting to combat isolation and low mood",
                    duration_minutes=20,
                    interactive_elements=["nature walks", "sunlight exposure", "fresh air"],
                    goals=["mood improvement", "vitamin D", "nature connection"]
                )
            ],
            
            MoodCategory.ANGRY: [
                SceneRecommendation(
                    scene_type=SceneType.VIRTUAL_GYM,
                    therapy_technique=TherapyTechnique.PHYSICAL_ACTIVITY,
                    priority=10,
                    description="Safe space for physical release of anger",
                    duration_minutes=15,
                    interactive_elements=["punching bags", "cardio equipment", "anger tracking"],
                    goals=["healthy anger release", "physical outlet", "energy discharge"]
                ),
                SceneRecommendation(
                    scene_type=SceneType.MOUNTAIN_RETREAT,
                    therapy_technique=TherapyTechnique.PROGRESSIVE_MUSCLE_RELAXATION,
                    priority=8,
                    description="Mountain setting for tension release and perspective",
                    duration_minutes=20,
                    interactive_elements=["muscle relaxation guide", "tension tracking", "calm visuals"],
                    goals=["physical tension release", "emotional regulation", "perspective gain"]
                ),
                SceneRecommendation(
                    scene_type=SceneType.BREATHING_GARDEN,
                    therapy_technique=TherapyTechnique.BREATHING_EXERCISES,
                    priority=7,
                    description="Cooling down space with anger management breathing",
                    duration_minutes=10,
                    interactive_elements=["anger-specific breathing", "cool-down timer", "progress tracking"],
                    goals=["immediate calming", "anger management", "self-control"]
                )
            ],
            
            MoodCategory.STRESSED: [
                SceneRecommendation(
                    scene_type=SceneType.PEACEFUL_BEACH,
                    therapy_technique=TherapyTechnique.PROGRESSIVE_MUSCLE_RELAXATION,
                    priority=9,
                    description="Beach environment for stress relief and relaxation",
                    duration_minutes=20,
                    interactive_elements=["wave sounds", "muscle relaxation", "stress meter"],
                    goals=["stress reduction", "muscle relaxation", "mental reset"]
                ),
                SceneRecommendation(
                    scene_type=SceneType.FOREST_MEDITATION,
                    therapy_technique=TherapyTechnique.MINDFULNESS_MEDITATION,
                    priority=8,
                    description="Forest setting for stress-focused mindfulness",
                    duration_minutes=15,
                    interactive_elements=["nature sounds", "stress-specific meditation", "focus aids"],
                    goals=["mindful awareness", "stress management", "mental clarity"]
                ),
                SceneRecommendation(
                    scene_type=SceneType.BREATHING_GARDEN,
                    therapy_technique=TherapyTechnique.BREATHING_EXERCISES,
                    priority=8,
                    description="Garden space for stress-relief breathing techniques",
                    duration_minutes=12,
                    interactive_elements=["stress breathing patterns", "heart rate monitoring", "relaxation cues"],
                    goals=["immediate stress relief", "breathing mastery", "physiological calming"]
                )
            ],
            
            MoodCategory.LONELY: [
                SceneRecommendation(
                    scene_type=SceneType.SOCIAL_CAFÉ,
                    therapy_technique=TherapyTechnique.SOCIAL_INTERACTION,
                    priority=10,
                    description="Virtual café for social connection practice",
                    duration_minutes=25,
                    interactive_elements=["virtual companions", "conversation practice", "social cues"],
                    goals=["combat loneliness", "social skills", "connection feeling"]
                ),
                SceneRecommendation(
                    scene_type=SceneType.COZY_INDOOR,
                    therapy_technique=TherapyTechnique.COGNITIVE_RESTRUCTURING,
                    priority=8,
                    description="Safe space to work through loneliness thoughts",
                    duration_minutes=20,
                    interactive_elements=["thought challenges", "loneliness coping", "self-compassion"],
                    goals=["address loneliness thoughts", "self-connection", "emotional support"]
                ),
                SceneRecommendation(
                    scene_type=SceneType.ART_THERAPY_STUDIO,
                    therapy_technique=TherapyTechnique.GUIDED_IMAGERY,
                    priority=7,
                    description="Creative space for self-expression and connection",
                    duration_minutes=30,
                    interactive_elements=["creative expression", "self-discovery", "meaning-making"],
                    goals=["self-expression", "inner connection", "purpose finding"]
                )
            ],
            
            MoodCategory.HAPPY: [
                SceneRecommendation(
                    scene_type=SceneType.CALMING_NATURE,
                    therapy_technique=TherapyTechnique.MINDFULNESS_MEDITATION,
                    priority=8,
                    description="Nature setting to maintain and enhance positive mood",
                    duration_minutes=15,
                    interactive_elements=["gratitude practice", "positive focus", "joy cultivation"],
                    goals=["mood maintenance", "gratitude practice", "positive reinforcement"]
                ),
                SceneRecommendation(
                    scene_type=SceneType.VIRTUAL_GYM,
                    therapy_technique=TherapyTechnique.PHYSICAL_ACTIVITY,
                    priority=7,
                    description="Active space to channel positive energy",
                    duration_minutes=20,
                    interactive_elements=["energizing activities", "goal setting", "achievement tracking"],
                    goals=["energy channeling", "goal achievement", "positive momentum"]
                )
            ],
            
            MoodCategory.NEUTRAL: [
                SceneRecommendation(
                    scene_type=SceneType.COZY_INDOOR,
                    therapy_technique=TherapyTechnique.MINDFULNESS_MEDITATION,
                    priority=7,
                    description="Gentle introduction to mindfulness practice",
                    duration_minutes=15,
                    interactive_elements=["basic mindfulness", "mood check-in", "gentle guidance"],
                    goals=["mindfulness introduction", "mood awareness", "self-discovery"]
                ),
                SceneRecommendation(
                    scene_type=SceneType.CALMING_NATURE,
                    therapy_technique=TherapyTechnique.NATURE_THERAPY,
                    priority=6,
                    description="Nature exploration for general wellbeing",
                    duration_minutes=20,
                    interactive_elements=["nature exploration", "relaxation", "general wellness"],
                    goals=["general wellness", "mood enhancement", "nature connection"]
                )
            ],
            
            MoodCategory.FRUSTRATED: [
                SceneRecommendation(
                    scene_type=SceneType.VIRTUAL_GYM,
                    therapy_technique=TherapyTechnique.PHYSICAL_ACTIVITY,
                    priority=9,
                    description="Safe space for physical release of frustration",
                    duration_minutes=15,
                    interactive_elements=["punching bags", "cardio equipment", "frustration tracking"],
                    goals=["healthy frustration release", "physical outlet", "energy discharge"]
                ),
                SceneRecommendation(
                    scene_type=SceneType.BREATHING_GARDEN,
                    therapy_technique=TherapyTechnique.BREATHING_EXERCISES,
                    priority=8,
                    description="Calming garden for frustration management",
                    duration_minutes=12,
                    interactive_elements=["calming breathing", "tension release", "patience building"],
                    goals=["immediate calming", "frustration management", "patience development"]
                )
            ],
            
            MoodCategory.OVERWHELMED: [
                SceneRecommendation(
                    scene_type=SceneType.PEACEFUL_BEACH,
                    therapy_technique=TherapyTechnique.GROUNDING_TECHNIQUES,
                    priority=10,
                    description="Beach environment for grounding and perspective",
                    duration_minutes=18,
                    interactive_elements=["5-4-3-2-1 grounding", "ocean sounds", "visual anchors"],
                    goals=["reduce overwhelm", "ground in present", "gain perspective"]
                ),
                SceneRecommendation(
                    scene_type=SceneType.MOUNTAIN_RETREAT,
                    therapy_technique=TherapyTechnique.MINDFULNESS_MEDITATION,
                    priority=8,
                    description="Mountain setting for clarity and space",
                    duration_minutes=20,
                    interactive_elements=["space meditation", "clarity practice", "simplification"],
                    goals=["mental clarity", "overwhelm reduction", "priority setting"]
                )
            ],
            
            MoodCategory.NEUTRAL: [
                SceneRecommendation(
                    scene_type=SceneType.COZY_INDOOR,
                    therapy_technique=TherapyTechnique.MINDFULNESS_MEDITATION,
                    priority=7,
                    description="Gentle introduction to mindfulness practice",
                    duration_minutes=15,
                    interactive_elements=["basic mindfulness", "mood check-in", "gentle guidance"],
                    goals=["mindfulness introduction", "mood awareness", "self-discovery"]
                ),
                SceneRecommendation(
                    scene_type=SceneType.CALMING_NATURE,
                    therapy_technique=TherapyTechnique.NATURE_THERAPY,
                    priority=6,
                    description="Nature exploration for general wellbeing",
                    duration_minutes=20,
                    interactive_elements=["nature exploration", "relaxation", "general wellness"],
                    goals=["general wellness", "mood enhancement", "nature connection"]
                )
            ]
        }
    
    def get_scene_recommendations(self, mood: MoodCategory, user_preferences: Optional[Dict] = None) -> List[SceneRecommendation]:
        """Get scene recommendations for a specific mood"""
        recommendations = self.mood_mappings.get(mood, [])
        
        # Apply user preferences if provided
        if user_preferences:
            recommendations = self._filter_by_preferences(recommendations, user_preferences)
        
        # Sort by priority (highest first)
        return sorted(recommendations, key=lambda x: x.priority, reverse=True)
    
    def _filter_by_preferences(self, recommendations: List[SceneRecommendation], preferences: Dict) -> List[SceneRecommendation]:
        """Filter recommendations based on user preferences"""
        filtered = []
        
        for rec in recommendations:
            # Check duration preference
            if 'max_duration' in preferences:
                if rec.duration_minutes > preferences['max_duration']:
                    continue
            
            # Check scene type preference
            if 'preferred_scenes' in preferences:
                if rec.scene_type.value not in preferences['preferred_scenes']:
                    continue
            
            # Check therapy technique preference
            if 'preferred_techniques' in preferences:
                if rec.therapy_technique.value not in preferences['preferred_techniques']:
                    continue
            
            filtered.append(rec)
        
        return filtered
    
    def analyze_mood_for_backend(self, mood_text: str, intensity: int = 5, user_preferences: Optional[Dict] = None) -> MoodAnalysisResult:
        """Complete mood analysis for backend integration"""
        # This would integrate with the existing analyze_mood function
        from app.models.therapy_bot import analyze_mood
        
        # Get primary mood
        primary_mood_text = analyze_mood(mood_text)
        primary_mood = self._text_to_mood_category(primary_mood_text)
        
        # Get scene recommendations
        scene_recommendations = self.get_scene_recommendations(primary_mood, user_preferences)
        
        # Determine crisis risk based on mood and text
        crisis_risk = self._assess_crisis_risk(mood_text, primary_mood, intensity)
        
        # Generate therapeutic goals
        therapeutic_goals = self._generate_therapeutic_goals(primary_mood, intensity)
        
        return MoodAnalysisResult(
            primary_mood=primary_mood,
            confidence_score=0.8,  # Would be calculated based on analysis quality
            secondary_moods=[],  # Could be enhanced to detect multiple moods
            intensity=intensity,
            crisis_risk=crisis_risk,
            scene_recommendations=scene_recommendations[:3],  # Top 3 recommendations
            therapeutic_goals=therapeutic_goals,
            session_metadata={
                "timestamp": str(__import__('datetime').datetime.now()),
                "mood_text": mood_text
            }
        )
    
    def _text_to_mood_category(self, mood_text: str) -> MoodCategory:
        """Convert mood text to MoodCategory enum"""
        mood_mapping = {
            "happy": MoodCategory.HAPPY,
            "sad": MoodCategory.SAD,
            "anxious": MoodCategory.ANXIOUS,
            "angry": MoodCategory.ANGRY,
            "stressed": MoodCategory.STRESSED,
            "depressed": MoodCategory.DEPRESSED,
            "neutral": MoodCategory.NEUTRAL,
            "frustrated": MoodCategory.FRUSTRATED,
            "lonely": MoodCategory.LONELY,
            "overwhelmed": MoodCategory.OVERWHELMED
        }
        
        return mood_mapping.get(mood_text.lower(), MoodCategory.NEUTRAL)
    
    def _assess_crisis_risk(self, text: str, mood: MoodCategory, intensity: int) -> bool:
        """Assess if there's a crisis risk requiring immediate intervention"""
        crisis_keywords = [
            "suicide", "kill myself", "end it all", "no point", "hurt myself",
            "self harm", "self-harm", "cutting", "overdose", "can't go on"
        ]
        
        text_lower = text.lower()
        has_crisis_keywords = any(keyword in text_lower for keyword in crisis_keywords)
        
        # High intensity negative moods with crisis keywords
        high_risk_moods = [MoodCategory.DEPRESSED, MoodCategory.ANGRY]
        high_intensity_risk = mood in high_risk_moods and intensity >= 8
        
        return has_crisis_keywords or high_intensity_risk
    
    def _generate_therapeutic_goals(self, mood: MoodCategory, intensity: int) -> List[str]:
        """Generate therapeutic goals based on mood and intensity"""
        base_goals = {
            MoodCategory.ANXIOUS: ["Reduce anxiety levels", "Learn coping strategies", "Build confidence"],
            MoodCategory.DEPRESSED: ["Improve mood", "Challenge negative thoughts", "Increase self-compassion"],
            MoodCategory.ANGRY: ["Manage anger effectively", "Learn healthy expression", "Develop self-control"],
            MoodCategory.STRESSED: ["Reduce stress levels", "Develop relaxation skills", "Improve work-life balance"],
            MoodCategory.LONELY: ["Build social connections", "Improve self-relationship", "Develop social skills"],
            MoodCategory.HAPPY: ["Maintain positive mood", "Practice gratitude", "Build resilience"],
            MoodCategory.NEUTRAL: ["Increase self-awareness", "Explore emotions", "Develop coping skills"]
        }
        
        goals = base_goals.get(mood, ["General wellbeing", "Self-awareness"])
        
        # Add intensity-specific goals
        if intensity >= 8:
            goals.append("Immediate symptom relief")
        elif intensity <= 3:
            goals.append("Mood enhancement")
        
        return goals
    
    def export_for_backend(self, analysis_result: MoodAnalysisResult) -> Dict:
        """Export analysis result in a format suitable for Java backend"""
        return {
            "moodAnalysis": {
                "primaryMood": analysis_result.primary_mood.value,
                "confidenceScore": analysis_result.confidence_score,
                "intensity": analysis_result.intensity,
                "crisisRisk": analysis_result.crisis_risk,
                "therapeuticGoals": analysis_result.therapeutic_goals
            },
            "sceneRecommendations": [
                {
                    "sceneType": rec.scene_type.value,
                    "therapyTechnique": rec.therapy_technique.value,
                    "priority": rec.priority,
                    "description": rec.description,
                    "durationMinutes": rec.duration_minutes,
                    "interactiveElements": rec.interactive_elements,
                    "goals": rec.goals
                }
                for rec in analysis_result.scene_recommendations
            ],
            "sessionMetadata": analysis_result.session_metadata
        }

# Global instance for use across the application
mood_scene_mapper = MoodSceneMapper()
