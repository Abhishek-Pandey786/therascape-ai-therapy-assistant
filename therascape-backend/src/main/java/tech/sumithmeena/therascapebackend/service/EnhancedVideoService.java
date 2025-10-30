package tech.sumithmeena.therascapebackend.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import tech.sumithmeena.therascapebackend.model.EnhancedVideo;
import tech.sumithmeena.therascapebackend.repository.EnhancedVideoRepository;

import java.util.*;
import java.util.stream.Collectors;

@Service
public class EnhancedVideoService {

    @Autowired
    private EnhancedVideoRepository enhancedVideoRepository;

    public List<EnhancedVideo> getPersonalizedVideoRecommendations(
            String username, String moodCategory, int moodIntensity,
            boolean crisisRisk, int maxDuration) {

        // Get user preferences (this could be expanded to store user preferences)
        // Optional<User> userOpt = userRepository.findByUsername(username);

        List<EnhancedVideo> recommendations = new ArrayList<>();

        // Priority 1: Crisis-safe content if user is in crisis
        if (crisisRisk) {
            recommendations.addAll(
                    enhancedVideoRepository.findCrisisSafeByMoodCategory(moodCategory)
                            .stream()
                            .filter(video -> video.getDurationMinutes() <= maxDuration)
                            .limit(3)
                            .collect(Collectors.toList()));
        }

        // Priority 2: Intensity-matched content
        List<EnhancedVideo> intensityMatched = enhancedVideoRepository
                .findByMoodCategoryAndIntensity(moodCategory, moodIntensity)
                .stream()
                .filter(video -> video.getDurationMinutes() <= maxDuration)
                .collect(Collectors.toList());

        recommendations.addAll(intensityMatched);

        // Priority 3: General mood category content
        if (recommendations.size() < 5) {
            List<EnhancedVideo> generalMood = enhancedVideoRepository
                    .findByPrimaryMoodCategoryIgnoreCase(moodCategory)
                    .stream()
                    .filter(video -> video.getDurationMinutes() <= maxDuration)
                    .filter(video -> !recommendations.contains(video))
                    .collect(Collectors.toList());

            recommendations.addAll(generalMood);
        }

        // Remove duplicates and sort by relevance
        return recommendations.stream()
                .distinct()
                .sorted(this::compareVideoRelevance)
                .limit(10)
                .collect(Collectors.toList());
    }

    public List<EnhancedVideo> getVideosByTherapeuticGoals(List<String> therapeuticGoals) {
        return enhancedVideoRepository.findByTherapeuticGoalsIn(therapeuticGoals)
                .stream()
                .sorted((v1, v2) -> Double.compare(v2.getAverageRating(), v1.getAverageRating()))
                .collect(Collectors.toList());
    }

    public List<EnhancedVideo> getBeginnerFriendlyVideos(String moodCategory) {
        return enhancedVideoRepository.findByMoodCategoryAndDifficulty(moodCategory, "beginner")
                .stream()
                .filter(video -> video.getDurationMinutes() <= 15) // Short videos for beginners
                .sorted((v1, v2) -> Double.compare(v2.getAverageRating(), v1.getAverageRating()))
                .collect(Collectors.toList());
    }

    public List<EnhancedVideo> getVideosByContentType(String contentType, String moodCategory) {
        return enhancedVideoRepository.findByContentTypeIgnoreCase(contentType)
                .stream()
                .filter(video -> video.getPrimaryMoodCategory().equalsIgnoreCase(moodCategory))
                .sorted(this::compareVideoRelevance)
                .collect(Collectors.toList());
    }

    public List<EnhancedVideo> getQuickHelpVideos(String moodCategory) {
        // Videos under 10 minutes for immediate help
        return enhancedVideoRepository.findByMoodCategoryAndMaxDuration(moodCategory, 10)
                .stream()
                .sorted((v1, v2) -> {
                    // Prioritize by completion rate and rating
                    double score1 = v1.getCompletionRate() * 0.6 + v1.getAverageRating() * 0.4;
                    double score2 = v2.getCompletionRate() * 0.6 + v2.getAverageRating() * 0.4;
                    return Double.compare(score2, score1);
                })
                .limit(5)
                .collect(Collectors.toList());
    }

    public List<EnhancedVideo> getScenarioBasedVideos(String scenarioType, String moodCategory) {
        return enhancedVideoRepository.findByScenarioTypeIgnoreCase(scenarioType)
                .stream()
                .filter(video -> video.getPrimaryMoodCategory().equalsIgnoreCase(moodCategory))
                .sorted(this::compareVideoRelevance)
                .collect(Collectors.toList());
    }

    public void recordVideoInteraction(String videoId, String username, String interactionType) {
        // This would record user interactions for improving recommendations
        // interactionType: "view", "complete", "like", "skip", etc.

        Optional<EnhancedVideo> videoOpt = enhancedVideoRepository.findById(videoId);
        if (videoOpt.isPresent()) {
            EnhancedVideo video = videoOpt.get();

            switch (interactionType.toLowerCase()) {
                case "view":
                    video.setViewCount(video.getViewCount() + 1);
                    break;
                case "like":
                    video.setLikeCount(video.getLikeCount() + 1);
                    break;
                case "complete":
                    // Update completion rate logic would go here
                    break;
            }

            enhancedVideoRepository.save(video);
        }
    }

    public List<EnhancedVideo> getPopularVideos(String moodCategory, int limit) {
        return enhancedVideoRepository.findPopularByMoodCategory(moodCategory)
                .stream()
                .sorted((v1, v2) -> {
                    // Combine multiple metrics for popularity score
                    double score1 = calculatePopularityScore(v1);
                    double score2 = calculatePopularityScore(v2);
                    return Double.compare(score2, score1);
                })
                .limit(limit)
                .collect(Collectors.toList());
    }

    private double calculatePopularityScore(EnhancedVideo video) {
        // Weighted scoring system
        double ratingWeight = 0.3;
        double viewWeight = 0.25;
        double completionWeight = 0.25;
        double likeWeight = 0.2;

        double normalizedRating = video.getAverageRating() / 5.0; // Assuming 5-star rating
        double normalizedViews = Math.min(video.getViewCount() / 1000.0, 1.0); // Cap at 1000 views
        double normalizedCompletion = video.getCompletionRate();
        double normalizedLikes = Math.min(video.getLikeCount() / 100.0, 1.0); // Cap at 100 likes

        return (normalizedRating * ratingWeight) +
                (normalizedViews * viewWeight) +
                (normalizedCompletion * completionWeight) +
                (normalizedLikes * likeWeight);
    }

    private int compareVideoRelevance(EnhancedVideo v1, EnhancedVideo v2) {
        // Custom comparison logic for video relevance
        double score1 = calculatePopularityScore(v1);
        double score2 = calculatePopularityScore(v2);
        return Double.compare(score2, score1);
    }

    public List<EnhancedVideo> getAllActiveVideos() {
        return enhancedVideoRepository.findByIsActiveTrueOrderByAverageRatingDesc();
    }

    public EnhancedVideo saveVideo(EnhancedVideo video) {
        return enhancedVideoRepository.save(video);
    }

    public Optional<EnhancedVideo> getVideoById(String id) {
        return enhancedVideoRepository.findById(id);
    }
}
