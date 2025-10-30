package tech.sumithmeena.therascapebackend.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "videos")
public class Video {
    @Id
    private String id;

    private String moodCategory;
    private String videoUrl;
    private String title;
    private String description;

    // Getters and setters
    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getMoodCategory() {
        return moodCategory;
    }

    public void setMoodCategory(String moodCategory) {
        this.moodCategory = moodCategory;
    }

    public String getVideoUrl() {
        return videoUrl;
    }

    public void setVideoUrl(String videoUrl) {
        this.videoUrl = videoUrl;
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

    // All-args constructor
    public Video(String id, String moodCategory, String videoUrl, String title, String description) {
        this.id = id;
        this.moodCategory = moodCategory;
        this.videoUrl = videoUrl;
        this.title = title;
        this.description = description;
    }

    // No-args constructor
    public Video() {
    }
}
