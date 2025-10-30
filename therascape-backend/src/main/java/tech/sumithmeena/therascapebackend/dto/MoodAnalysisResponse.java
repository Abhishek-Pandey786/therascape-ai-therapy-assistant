package tech.sumithmeena.therascapebackend.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class MoodAnalysisResponse {
    private boolean success;
    private String primaryMood;
    private Double confidenceScore;
    private Integer intensity;
    private Boolean crisisRisk;
    private List<String> therapeuticGoals;
    private List<SceneRecommendation> sceneRecommendations;
    private LocalDateTime timestamp;
    private String message;

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class SceneRecommendation {
        private String sceneType;
        private String therapyTechnique;
        private Integer priority;
        private String description;
        private Integer durationMinutes;
        private List<String> interactiveElements;
        private List<String> goals;
    }
}
