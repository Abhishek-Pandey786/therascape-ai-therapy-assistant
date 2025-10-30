package tech.sumithmeena.therascapebackend.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Map;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class MoodAnalysisRequest {
    private String text;
    private Integer intensity; // 1-10 scale
    private Map<String, Object> preferences;
    private Long userId;
    private String sessionId;
}
