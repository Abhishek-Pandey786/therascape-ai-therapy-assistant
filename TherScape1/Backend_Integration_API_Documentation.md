# TheraScape AI - Backend Integration API Documentation

## Overview

This document provides comprehensive information for integrating the TheraScape AI therapy chatbot with the Java backend and Unity AR/VR components. The API provides standardized mood analysis, scene recommendations, and therapeutic guidance.

## Base URL

```
http://localhost:5000/api
```

## Authentication

Currently no authentication required for local development. For production, implement appropriate authentication mechanisms.

---

## Core API Endpoints

### 1. Comprehensive Mood Analysis

**Endpoint:** `POST /api/mood-analysis`

**Purpose:** Analyze user text for mood, intensity, crisis risk, and get scene recommendations.

**Request Body:**

```json
{
  "text": "I'm feeling really overwhelmed with work and can't sleep",
  "intensity": 7,
  "preferences": {
    "max_duration": 20,
    "preferred_scenes": ["calming_nature", "peaceful_beach"],
    "preferred_techniques": ["breathing_exercises", "mindfulness_meditation"]
  }
}
```

**Response:**

```json
{
  "analysis": {
    "moodAnalysis": {
      "primaryMood": "stressed",
      "confidenceScore": 0.8,
      "intensity": 7,
      "crisisRisk": false,
      "therapeuticGoals": [
        "Reduce stress levels",
        "Develop relaxation skills",
        "Improve work-life balance"
      ]
    },
    "sceneRecommendations": [
      {
        "sceneType": "peaceful_beach",
        "therapyTechnique": "progressive_muscle_relaxation",
        "priority": 9,
        "description": "Beach environment for stress relief and relaxation",
        "durationMinutes": 20,
        "interactiveElements": [
          "wave sounds",
          "muscle relaxation",
          "stress meter"
        ],
        "goals": ["stress reduction", "muscle relaxation", "mental reset"]
      }
    ],
    "sessionMetadata": {
      "timestamp": "2024-01-15T10:30:00",
      "mood_text": "I'm feeling really overwhelmed with work and can't sleep"
    }
  },
  "success": true
}
```

### 2. Scene Recommendations by Mood

**Endpoint:** `GET /api/scene-recommendations/{mood}`

**Purpose:** Get therapeutic scene recommendations for a specific mood category.

**URL Parameters:**

- `mood` (required): One of the standardized mood categories

**Query Parameters:**

- `max_duration`: Maximum session duration in minutes
- `preferred_scenes`: Comma-separated list of preferred scene types
- `preferred_techniques`: Comma-separated list of preferred therapy techniques

**Example:**

```
GET /api/scene-recommendations/anxious?max_duration=15&preferred_scenes=calming_nature,peaceful_beach
```

**Response:**

```json
{
  "mood": "anxious",
  "recommendations": [
    {
      "sceneType": "breathing_garden",
      "therapyTechnique": "breathing_exercises",
      "priority": 10,
      "description": "Peaceful garden environment with guided breathing exercises",
      "durationMinutes": 10,
      "interactiveElements": [
        "breathing guide",
        "calming sounds",
        "visual cues"
      ],
      "goals": ["reduce anxiety", "practice breathing", "immediate calming"]
    }
  ],
  "count": 1,
  "success": true
}
```

### 3. Crisis Risk Assessment

**Endpoint:** `POST /api/crisis-assessment`

**Purpose:** Assess crisis risk and get immediate intervention recommendations.

**Request Body:**

```json
{
  "text": "I can't take this anymore, there's no point",
  "mood": "depressed",
  "intensity": 9
}
```

**Response:**

```json
{
  "crisis_risk": true,
  "risk_level": "HIGH",
  "interventions": [
    "Immediate professional support recommended",
    "Crisis hotline: 988 (US) or local emergency services",
    "Do not leave person alone if possible"
  ],
  "immediate_action_required": true,
  "success": true
}
```

### 4. Available Categories and Types

**Endpoints:**

- `GET /api/mood-categories` - Get all mood categories
- `GET /api/therapy-techniques` - Get all therapy techniques
- `GET /api/scene-types` - Get all scene types

---

## Standardized Data Types

### Mood Categories

```
happy, sad, anxious, angry, stressed, depressed, neutral, frustrated, lonely, overwhelmed
```

### Scene Types

```
calming_nature, peaceful_beach, forest_meditation, mountain_retreat, cozy_indoor,
breathing_garden, social_cafe, virtual_gym, art_therapy_studio, confidence_stage
```

### Therapy Techniques

```
breathing_exercises, mindfulness_meditation, progressive_muscle_relaxation,
guided_imagery, grounding_techniques, cognitive_restructuring, exposure_therapy,
nature_therapy, social_interaction, physical_activity
```

---

## Integration Guidelines for Java Backend

### 1. Mood-to-Scene Pipeline

```java
// Example Java integration flow
public class TheraScapeIntegration {

    public SceneRecommendation getSceneForUser(String userInput, UserPreferences prefs) {
        // 1. Call mood analysis API
        MoodAnalysisResult analysis = callMoodAnalysisAPI(userInput, prefs);

        // 2. Check for crisis risk
        if (analysis.isCrisisRisk()) {
            return handleCrisisScenario(analysis);
        }

        // 3. Select top scene recommendation
        SceneRecommendation topScene = analysis.getSceneRecommendations().get(0);

        // 4. Load Unity scene with parameters
        return loadUnityScene(topScene);
    }

    private UnitySceneData loadUnityScene(SceneRecommendation scene) {
        return UnitySceneData.builder()
            .sceneType(scene.getSceneType())
            .duration(scene.getDurationMinutes())
            .interactiveElements(scene.getInteractiveElements())
            .therapyTechnique(scene.getTherapyTechnique())
            .goals(scene.getGoals())
            .build();
    }
}
```

### 2. Real-time Mood Tracking

```java
// Track user mood over time for progress monitoring
public class MoodTracker {

    public void trackMoodProgression(String userId, MoodAnalysisResult analysis) {
        MoodEntry entry = new MoodEntry(
            userId,
            analysis.getPrimaryMood(),
            analysis.getIntensity(),
            analysis.getConfidenceScore(),
            Instant.now()
        );

        moodRepository.save(entry);

        // Trigger alerts for concerning patterns
        checkForProgressConcerns(userId, entry);
    }
}
```

### 3. Scene Adaptation Logic

```java
public class SceneAdapter {

    public AdaptedScene adaptSceneForUser(SceneRecommendation base, UserContext context) {
        AdaptedScene adapted = new AdaptedScene(base);

        // Adjust based on user's therapy progress
        if (context.getSessionCount() > 10) {
            adapted.increaseDifficulty();
        }

        // Adjust based on time of day
        if (isEvening(context.getCurrentTime())) {
            adapted.addRelaxationElements();
        }

        // Adjust based on previous session outcomes
        if (context.getLastSessionRating() < 3) {
            adapted.simplifyChallenges();
        }

        return adapted;
    }
}
```

---

## Unity Integration Specifications

### Scene Loading Parameters

```csharp
[System.Serializable]
public class TheraSceneConfig
{
    public string sceneType;
    public string therapyTechnique;
    public int durationMinutes;
    public List<string> interactiveElements;
    public List<string> goals;
    public int priority;
    public string description;
}
```

### Scene Type Mappings

```csharp
public enum UnitySceneMapping
{
    calming_nature = "Scenes/Nature/CalmingForest",
    peaceful_beach = "Scenes/Beach/PeacefulShore",
    forest_meditation = "Scenes/Forest/MeditationGrove",
    mountain_retreat = "Scenes/Mountain/Retreat",
    cozy_indoor = "Scenes/Indoor/CozyRoom",
    breathing_garden = "Scenes/Garden/BreathingSpace",
    social_cafe = "Scenes/Social/VirtualCafe",
    virtual_gym = "Scenes/Activity/VirtualGym",
    art_therapy_studio = "Scenes/Creative/ArtStudio",
    confidence_stage = "Scenes/Performance/ConfidenceStage"
}
```

---

## Error Handling

### Standard Error Response

```json
{
  "error": "Description of error",
  "error_code": "MOOD_ANALYSIS_FAILED",
  "success": false,
  "timestamp": "2024-01-15T10:30:00"
}
```

### Common Error Codes

- `INVALID_MOOD_CATEGORY`: Unknown mood category provided
- `MOOD_ANALYSIS_FAILED`: AI mood analysis service unavailable
- `MISSING_REQUIRED_FIELD`: Required request field missing
- `CRISIS_INTERVENTION_REQUIRED`: Crisis detected, immediate action needed

---

## Testing and Validation

### Sample Test Cases

```bash
# Test mood analysis
curl -X POST http://localhost:5000/api/mood-analysis \
  -H "Content-Type: application/json" \
  -d '{"text": "I feel anxious about my presentation tomorrow", "intensity": 6}'

# Test scene recommendations
curl http://localhost:5000/api/scene-recommendations/anxious?max_duration=15

# Test crisis assessment
curl -X POST http://localhost:5000/api/crisis-assessment \
  -H "Content-Type: application/json" \
  -d '{"text": "I feel hopeless", "mood": "depressed", "intensity": 8}'
```

---

## Production Considerations

### 1. Performance Optimization

- Implement caching for scene recommendations
- Use connection pooling for database operations
- Consider async processing for mood analysis

### 2. Security

- Add API authentication (JWT tokens recommended)
- Implement rate limiting
- Validate and sanitize all input data
- Use HTTPS in production

### 3. Monitoring

- Log all mood analyses for improvement
- Monitor crisis detection accuracy
- Track scene recommendation effectiveness
- Set up alerts for system failures

### 4. Data Privacy

- Implement user data encryption
- Follow HIPAA guidelines for health data
- Provide user data deletion capabilities
- Regular security audits

---

## Support and Maintenance

For technical support or questions about the API integration, please contact:

- API Documentation: [GitHub Repository]
- Bug Reports: [Issue Tracker]
- Feature Requests: [Feature Request Form]

## Version History

- v1.0.0: Initial API release with mood analysis and scene recommendations
- v1.1.0: Added crisis assessment and user preferences (Current)
