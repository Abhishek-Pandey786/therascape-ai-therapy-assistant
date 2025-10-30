package tech.sumithmeena.therascapebackend.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import java.util.List;
import java.time.LocalDateTime;

@Document(collection = "enhanced_videos")
public class EnhancedVideo {
    @Id
    private String id;

    // Basic video information
    private String title;
    private String description;
    private String videoUrl;
    private String thumbnailUrl;
    private int durationMinutes;

    // Mood and therapy targeting
    private String primaryMoodCategory;
    private List<String> secondaryMoodCategories;
    private String therapyTechnique;
    private int moodIntensityMin; // 1-10
    private int moodIntensityMax; // 1-10

    // Content classification
    private String contentType; // "meditation", "breathing", "therapy", "educational"
    private String scenarioType; // "nature", "indoor", "beach", "forest", etc.
    private List<String> therapeuticGoals;

    // Personalization factors
    private String difficultyLevel; // "beginner", "intermediate", "advanced"
    private List<String> triggers; // Content that might trigger certain users
    private boolean crisisSafe; // Safe for users in crisis

    // Engagement metrics
    private double averageRating;
    private int viewCount;
    private double completionRate;
    private int likeCount;

    // Metadata
    private LocalDateTime createdDate;
    private LocalDateTime lastUpdated;
    private String createdBy;
    private boolean isActive;

    // Interactive elements
    private List<String> interactiveFeatures; // "breathing guide", "progress tracker", etc.
    private boolean hasSubtitles;
    private List<String> availableLanguages;

    // Constructors
    public EnhancedVideo() {
    }

    public EnhancedVideo(String title, String videoUrl, String primaryMoodCategory,
            String therapyTechnique, int durationMinutes) {
        this.title = title;
        this.videoUrl = videoUrl;
        this.primaryMoodCategory = primaryMoodCategory;
        this.therapyTechnique = therapyTechnique;
        this.durationMinutes = durationMinutes;
        this.createdDate = LocalDateTime.now();
        this.isActive = true;
        this.crisisSafe = true;
    }

    // Getters and Setters
    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getVideoUrl() {
        return videoUrl;
    }

    public void setVideoUrl(String videoUrl) {
        this.videoUrl = videoUrl;
    }

    public String getThumbnailUrl() {
        return thumbnailUrl;
    }

    public void setThumbnailUrl(String thumbnailUrl) {
        this.thumbnailUrl = thumbnailUrl;
    }

    public int getDurationMinutes() {
        return durationMinutes;
    }

    public void setDurationMinutes(int durationMinutes) {
        this.durationMinutes = durationMinutes;
    }

    public String getPrimaryMoodCategory() {
        return primaryMoodCategory;
    }

    public void setPrimaryMoodCategory(String primaryMoodCategory) {
        this.primaryMoodCategory = primaryMoodCategory;
    }

    public List<String> getSecondaryMoodCategories() {
        return secondaryMoodCategories;
    }

    public void setSecondaryMoodCategories(List<String> secondaryMoodCategories) {
        this.secondaryMoodCategories = secondaryMoodCategories;
    }

    public String getTherapyTechnique() {
        return therapyTechnique;
    }

    public void setTherapyTechnique(String therapyTechnique) {
        this.therapyTechnique = therapyTechnique;
    }

    public int getMoodIntensityMin() {
        return moodIntensityMin;
    }

    public void setMoodIntensityMin(int moodIntensityMin) {
        this.moodIntensityMin = moodIntensityMin;
    }

    public int getMoodIntensityMax() {
        return moodIntensityMax;
    }

    public void setMoodIntensityMax(int moodIntensityMax) {
        this.moodIntensityMax = moodIntensityMax;
    }

    public String getContentType() {
        return contentType;
    }

    public void setContentType(String contentType) {
        this.contentType = contentType;
    }

    public String getScenarioType() {
        return scenarioType;
    }

    public void setScenarioType(String scenarioType) {
        this.scenarioType = scenarioType;
    }

    public List<String> getTherapeuticGoals() {
        return therapeuticGoals;
    }

    public void setTherapeuticGoals(List<String> therapeuticGoals) {
        this.therapeuticGoals = therapeuticGoals;
    }

    public String getDifficultyLevel() {
        return difficultyLevel;
    }

    public void setDifficultyLevel(String difficultyLevel) {
        this.difficultyLevel = difficultyLevel;
    }

    public List<String> getTriggers() {
        return triggers;
    }

    public void setTriggers(List<String> triggers) {
        this.triggers = triggers;
    }

    public boolean isCrisisSafe() {
        return crisisSafe;
    }

    public void setCrisisSafe(boolean crisisSafe) {
        this.crisisSafe = crisisSafe;
    }

    public double getAverageRating() {
        return averageRating;
    }

    public void setAverageRating(double averageRating) {
        this.averageRating = averageRating;
    }

    public int getViewCount() {
        return viewCount;
    }

    public void setViewCount(int viewCount) {
        this.viewCount = viewCount;
    }

    public double getCompletionRate() {
        return completionRate;
    }

    public void setCompletionRate(double completionRate) {
        this.completionRate = completionRate;
    }

    public int getLikeCount() {
        return likeCount;
    }

    public void setLikeCount(int likeCount) {
        this.likeCount = likeCount;
    }

    public LocalDateTime getCreatedDate() {
        return createdDate;
    }

    public void setCreatedDate(LocalDateTime createdDate) {
        this.createdDate = createdDate;
    }

    public LocalDateTime getLastUpdated() {
        return lastUpdated;
    }

    public void setLastUpdated(LocalDateTime lastUpdated) {
        this.lastUpdated = lastUpdated;
    }

    public String getCreatedBy() {
        return createdBy;
    }

    public void setCreatedBy(String createdBy) {
        this.createdBy = createdBy;
    }

    public boolean isActive() {
        return isActive;
    }

    public void setActive(boolean active) {
        isActive = active;
    }

    public List<String> getInteractiveFeatures() {
        return interactiveFeatures;
    }

    public void setInteractiveFeatures(List<String> interactiveFeatures) {
        this.interactiveFeatures = interactiveFeatures;
    }

    public boolean isHasSubtitles() {
        return hasSubtitles;
    }

    public void setHasSubtitles(boolean hasSubtitles) {
        this.hasSubtitles = hasSubtitles;
    }

    public List<String> getAvailableLanguages() {
        return availableLanguages;
    }

    public void setAvailableLanguages(List<String> availableLanguages) {
        this.availableLanguages = availableLanguages;
    }
}
