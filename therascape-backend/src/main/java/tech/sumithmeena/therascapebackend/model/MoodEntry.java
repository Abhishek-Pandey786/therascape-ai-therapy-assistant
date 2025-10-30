package tech.sumithmeena.therascapebackend.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.DBRef;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.LocalDateTime;

@Document(collection = "mood_entries")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class MoodEntry {

    @Id
    private String id;

    @DBRef
    private User user;

    private String userId; // Store user ID separately for easier querying

    private String primaryMood;

    private Integer intensity; // 1-10 scale

    private Double confidenceScore;

    private Boolean crisisRisk = false;

    private String originalText;

    private String sessionId;

    private LocalDateTime timestamp = LocalDateTime.now();

    private String therapeuticGoals;

    private String sceneRecommendations;

    public MoodEntry(User user, String primaryMood, Integer intensity, Double confidenceScore,
            LocalDateTime timestamp) {
        this.user = user;
        this.userId = user.getId();
        this.primaryMood = primaryMood;
        this.intensity = intensity;
        this.confidenceScore = confidenceScore;
        this.timestamp = timestamp;
    }
}
