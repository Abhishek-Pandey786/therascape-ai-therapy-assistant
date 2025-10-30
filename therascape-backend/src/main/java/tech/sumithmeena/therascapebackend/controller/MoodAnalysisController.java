package tech.sumithmeena.therascapebackend.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import tech.sumithmeena.therascapebackend.dto.MoodAnalysisRequest;
import tech.sumithmeena.therascapebackend.dto.MoodAnalysisResponse;
import tech.sumithmeena.therascapebackend.service.MoodAnalysisService;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/mood")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
public class MoodAnalysisController {

    private final MoodAnalysisService moodAnalysisService;

    @PostMapping("/analyze")
    public ResponseEntity<MoodAnalysisResponse> analyzeMood(@RequestBody MoodAnalysisRequest request) {
        try {
            MoodAnalysisResponse response = moodAnalysisService.analyzeMoodData(request);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }

    @GetMapping("/history/{userId}")
    public ResponseEntity<List<Map<String, Object>>> getMoodHistory(@PathVariable String userId) {
        try {
            List<Map<String, Object>> history = moodAnalysisService.getUserMoodHistory(userId);
            return ResponseEntity.ok(history);
        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }

    @GetMapping("/trends/{userId}")
    public ResponseEntity<Map<String, Object>> getMoodTrends(@PathVariable String userId) {
        try {
            Map<String, Object> trends = moodAnalysisService.getUserMoodTrends(userId);
            return ResponseEntity.ok(trends);
        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }
}
