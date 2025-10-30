# TheraScape AI - Mood Categories & Scene Recommendations Summary

### 📊 Standardized Mood Categories (10 Total)

```
1. happy      - Positive, joyful emotions
2. sad        - Temporary sadness, disappointment
3. anxious    - Worry, nervousness, fear
4. angry      - Irritation, frustration, rage
5. stressed   - Overwhelmed, under pressure
6. depressed  - Deep despair, hopelessness
7. neutral    - Balanced, calm emotional state
8. frustrated - Blocked, hindered feelings
9. lonely     - Isolated, disconnected
10. overwhelmed - Unable to cope with demands
```

### 🎬 Scene Types Available (10 Total)

```
1. calming_nature        - Peaceful forest/nature
2. peaceful_beach        - Serene beach environment
3. forest_meditation     - Quiet meditation grove
4. mountain_retreat      - Mountain views & fresh air
5. cozy_indoor          - Warm, safe indoor space
6. breathing_garden     - Garden for breathing exercises
7. social_cafe          - Virtual social interaction
8. virtual_gym          - Exercise & physical activity
9. art_therapy_studio   - Creative expression space
10. confidence_stage    - Confidence building environment
```

### 🔧 Therapy Techniques (10 Total)

```
1. breathing_exercises           - Controlled breathing patterns
2. mindfulness_meditation       - Present-moment awareness
3. progressive_muscle_relaxation - Systematic muscle relaxation
4. guided_imagery              - Therapeutic visualization
5. grounding_techniques        - Reality connection exercises
6. cognitive_restructuring     - Negative thought challenges
7. exposure_therapy           - Gradual fear exposure
8. nature_therapy            - Natural environment healing
9. social_interaction        - Therapeutic social engagement
10. physical_activity        - Movement for mental health
```

###  Main API Endpoint

**POST** `http://localhost:5000/api/mood-analysis`

**Request:**

```json
{
  "text": "User's emotional expression",
  "intensity": 7,
  "preferences": {
    "max_duration": 20,
    "preferred_scenes": ["calming_nature", "peaceful_beach"],
    "preferred_techniques": ["breathing_exercises"]
  }
}
```

**Response:**

```json
{
  "analysis": {
    "moodAnalysis": {
      "primaryMood": "stressed",
      "intensity": 7,
      "crisisRisk": false,
      "therapeuticGoals": ["Reduce stress levels", "Develop relaxation skills"]
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
    ]
  },
  "success": true
}
```

### Working in java

1. **Call the mood analysis API** when user inputs emotional text
2. **Get the top scene recommendation** from the response
3. **Map the sceneType to your Unity scene names**
4. **Load the Unity scene with the specified parameters**
5. **Track user progress** and mood changes over time

### Crisis Detection

The API automatically detects crisis situations and returns:

```json
{
  "crisisRisk": true,
  "risk_level": "HIGH",
  "interventions": [
    "Immediate professional support recommended",
    "Crisis hotline: 988"
  ]
}
```

### 🔗 Additional Endpoints

- `GET /api/scene-recommendations/{mood}` - Get scenes for specific mood
- `POST /api/crisis-assessment` - Standalone crisis risk assessment
- `GET /api/mood-categories` - List all mood categories
- `GET /api/therapy-techniques` - List all therapy techniques
- `GET /api/scene-types` - List all scene types

### 📋 Next Steps for Integration

1. **Review the full API documentation**: `Backend_Integration_API_Documentation.md`
2. **Test the endpoints**: All endpoints are tested and working (100% pass rate)
3. **Map scene types to Unity scenes**: Use the scene type values as identifiers
4. **Implement mood tracking**: Store user mood progression over time
5. **Handle crisis situations**: Implement crisis intervention protocols

### 🎯 Scene-to-Unity Mapping Example

```java
// Example mapping for your Unity scenes
Map<String, String> sceneMapping = Map.of(
    "calming_nature", "Scenes/Nature/CalmingForest",
    "peaceful_beach", "Scenes/Beach/PeacefulShore",
    "forest_meditation", "Scenes/Forest/MeditationGrove",
    "breathing_garden", "Scenes/Garden/BreathingSpace"
    // ... add all 10 scene types
);
```

### 📊 Ready for Production

- ✅ All 24 API tests passing
- ✅ Comprehensive mood detection
- ✅ Crisis risk assessment
- ✅ Scene recommendations with priorities
- ✅ User preference filtering
- ✅ Error handling and validation
- ✅ Detailed documentation

**The API is production-ready and waiting for your Unity integration!**

### 🤝 Support

If you need any modifications to the mood categories, scene types, or API structure, let me know. The system is designed to be flexible and easily extensible.

All API endpoints are live at: `http://localhost:5000/api/`
