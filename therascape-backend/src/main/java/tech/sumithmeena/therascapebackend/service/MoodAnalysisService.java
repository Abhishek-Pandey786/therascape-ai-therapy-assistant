package tech.sumithmeena.therascapebackend.service;

import org.springframework.stereotype.Service;
import tech.sumithmeena.therascapebackend.dto.MoodAnalysisRequest;
import tech.sumithmeena.therascapebackend.dto.MoodAnalysisResponse;

import java.time.LocalDateTime;
import java.util.*;

@Service
public class MoodAnalysisService {

    public MoodAnalysisResponse analyzeMoodData(MoodAnalysisRequest request) {
        try {
            // Basic mood analysis - can be enhanced with ML models
            String primaryMood = determinePrimaryMood(request.getText());
            double confidenceScore = calculateConfidence(request.getText(), primaryMood);
            boolean crisisRisk = assessCrisisRisk(request.getText(), request.getIntensity());

            List<String> therapeuticGoals = generateTherapeuticGoals(primaryMood, request.getIntensity());
            List<MoodAnalysisResponse.SceneRecommendation> sceneRecommendations = generateSceneRecommendations(
                    primaryMood, request.getPreferences());

            return new MoodAnalysisResponse(
                    true,
                    primaryMood,
                    confidenceScore,
                    request.getIntensity(),
                    crisisRisk,
                    therapeuticGoals,
                    sceneRecommendations,
                    LocalDateTime.now(),
                    "Mood analysis completed successfully");
        } catch (Exception e) {
            return new MoodAnalysisResponse(
                    false,
                    null,
                    null,
                    null,
                    false,
                    Collections.emptyList(),
                    Collections.emptyList(),
                    LocalDateTime.now(),
                    "Error analyzing mood: " + e.getMessage());
        }
    }

    public List<Map<String, Object>> getUserMoodHistory(String userId) {
        // Mock implementation - replace with actual database queries
        List<Map<String, Object>> history = new ArrayList<>();

        // Sample mood history data
        String[] moods = { "happy", "sad", "anxious", "calm", "stressed" };
        for (int i = 0; i < 7; i++) {
            Map<String, Object> entry = new HashMap<>();
            entry.put("date", LocalDateTime.now().minusDays(i).toLocalDate());
            entry.put("mood", moods[i % moods.length]);
            entry.put("intensity", 5 + (int) (Math.random() * 5));
            entry.put("notes", "Sample mood entry for day " + (i + 1));
            history.add(entry);
        }

        return history;
    }

    public Map<String, Object> getUserMoodTrends(String userId) {
        Map<String, Object> trends = new HashMap<>();

        // Sample trend data
        trends.put("averageIntensity", 6.2);
        trends.put("mostCommonMood", "calm");
        trends.put("improvementTrend", "positive");
        trends.put("weeklyAverage", 5.8);
        trends.put("monthlyAverage", 6.1);

        Map<String, Integer> moodDistribution = new HashMap<>();
        moodDistribution.put("happy", 25);
        moodDistribution.put("calm", 35);
        moodDistribution.put("anxious", 20);
        moodDistribution.put("sad", 15);
        moodDistribution.put("stressed", 5);

        trends.put("moodDistribution", moodDistribution);

        return trends;
    }

    private String determinePrimaryMood(String text) {
        if (text == null || text.trim().isEmpty()) {
            return "neutral";
        }

        String lowerText = text.toLowerCase();

        // Simple keyword-based mood detection
        if (lowerText.contains("sad") || lowerText.contains("down") || lowerText.contains("depressed")) {
            return "sad";
        } else if (lowerText.contains("anxious") || lowerText.contains("worried") || lowerText.contains("nervous")) {
            return "anxious";
        } else if (lowerText.contains("angry") || lowerText.contains("mad") || lowerText.contains("frustrated")) {
            return "angry";
        } else if (lowerText.contains("happy") || lowerText.contains("joy") || lowerText.contains("excited")) {
            return "happy";
        } else if (lowerText.contains("stressed") || lowerText.contains("overwhelmed")
                || lowerText.contains("pressure")) {
            return "stressed";
        } else if (lowerText.contains("lonely") || lowerText.contains("isolated") || lowerText.contains("alone")) {
            return "lonely";
        } else {
            return "neutral";
        }
    }

    private double calculateConfidence(String text, String mood) {
        // Simple confidence calculation based on text length and keyword matches
        if (text == null || text.trim().isEmpty()) {
            return 0.3;
        }

        int wordCount = text.split("\\s+").length;
        double baseConfidence = Math.min(0.5 + (wordCount * 0.02), 0.9);

        return Math.round(baseConfidence * 100.0) / 100.0;
    }

    private boolean assessCrisisRisk(String text, Integer intensity) {
        if (text == null || intensity == null) {
            return false;
        }

        String lowerText = text.toLowerCase();
        String[] crisisKeywords = {
                "suicide", "kill myself", "end it all", "can't go on",
                "no point", "hopeless", "want to die", "hurt myself"
        };

        for (String keyword : crisisKeywords) {
            if (lowerText.contains(keyword)) {
                return true;
            }
        }

        // High intensity (8+) with depressive mood indicators
        if (intensity >= 8 && (lowerText.contains("hopeless") || lowerText.contains("worthless"))) {
            return true;
        }

        return false;
    }

    private List<String> generateTherapeuticGoals(String mood, Integer intensity) {
        List<String> goals = new ArrayList<>();

        switch (mood.toLowerCase()) {
            case "anxious":
                goals.add("Reduce anxiety levels");
                goals.add("Practice relaxation techniques");
                goals.add("Develop coping strategies");
                break;
            case "sad":
                goals.add("Improve mood");
                goals.add("Increase positive activities");
                goals.add("Build emotional resilience");
                break;
            case "angry":
                goals.add("Manage anger effectively");
                goals.add("Practice emotional regulation");
                goals.add("Develop healthy expression");
                break;
            case "stressed":
                goals.add("Reduce stress levels");
                goals.add("Improve work-life balance");
                goals.add("Practice stress management");
                break;
            default:
                goals.add("Maintain emotional balance");
                goals.add("Continue self-care practices");
                goals.add("Build emotional awareness");
        }

        if (intensity != null && intensity >= 7) {
            goals.add("Seek additional support if needed");
        }

        return goals;
    }

    private List<MoodAnalysisResponse.SceneRecommendation> generateSceneRecommendations(
            String mood, Map<String, Object> preferences) {

        List<MoodAnalysisResponse.SceneRecommendation> recommendations = new ArrayList<>();

        switch (mood.toLowerCase()) {
            case "anxious":
                recommendations.add(new MoodAnalysisResponse.SceneRecommendation(
                        "breathing_garden",
                        "breathing_exercises",
                        10,
                        "Peaceful garden environment with guided breathing exercises",
                        10,
                        Arrays.asList("breathing guide", "calming sounds", "visual cues"),
                        Arrays.asList("reduce anxiety", "practice breathing", "immediate calming")));
                break;

            case "sad":
                recommendations.add(new MoodAnalysisResponse.SceneRecommendation(
                        "calming_nature",
                        "mindfulness_meditation",
                        9,
                        "Serene natural environment for mood lifting",
                        15,
                        Arrays.asList("nature sounds", "gentle lighting", "meditation guide"),
                        Arrays.asList("improve mood", "increase positivity", "emotional healing")));
                break;

            case "stressed":
                recommendations.add(new MoodAnalysisResponse.SceneRecommendation(
                        "peaceful_beach",
                        "progressive_muscle_relaxation",
                        9,
                        "Beach environment for stress relief and relaxation",
                        20,
                        Arrays.asList("wave sounds", "muscle relaxation", "stress meter"),
                        Arrays.asList("stress reduction", "muscle relaxation", "mental reset")));
                break;

            case "angry":
                recommendations.add(new MoodAnalysisResponse.SceneRecommendation(
                        "virtual_gym",
                        "physical_activity",
                        8,
                        "Virtual exercise space for energy release",
                        15,
                        Arrays.asList("punching bag", "cardio exercises", "anger meter"),
                        Arrays.asList("release anger", "physical exercise", "emotional regulation")));
                break;

            default:
                recommendations.add(new MoodAnalysisResponse.SceneRecommendation(
                        "cozy_indoor",
                        "guided_imagery",
                        7,
                        "Comfortable indoor space for general wellbeing",
                        12,
                        Arrays.asList("soft lighting", "comfortable seating", "calming music"),
                        Arrays.asList("maintain balance", "relaxation", "self-care")));
        }

        return recommendations;
    }
}
