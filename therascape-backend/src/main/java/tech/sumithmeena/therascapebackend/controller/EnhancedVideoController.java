package tech.sumithmeena.therascapebackend.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import tech.sumithmeena.therascapebackend.model.EnhancedVideo;
import tech.sumithmeena.therascapebackend.service.EnhancedVideoService;

import java.util.List;

@RestController
@RequestMapping("/api/enhanced-videos")
@CrossOrigin(origins = "*")
public class EnhancedVideoController {

    @Autowired
    private EnhancedVideoService enhancedVideoService;

    @GetMapping("/personalized/{username}")
    public ResponseEntity<List<EnhancedVideo>> getPersonalizedRecommendations(
            @PathVariable String username,
            @RequestParam String moodCategory,
            @RequestParam(defaultValue = "5") int moodIntensity,
            @RequestParam(defaultValue = "false") boolean crisisRisk,
            @RequestParam(defaultValue = "30") int maxDuration) {

        List<EnhancedVideo> recommendations = enhancedVideoService.getPersonalizedVideoRecommendations(
                username, moodCategory, moodIntensity, crisisRisk, maxDuration);

        return ResponseEntity.ok(recommendations);
    }

    @GetMapping("/therapeutic-goals")
    public ResponseEntity<List<EnhancedVideo>> getVideosByTherapeuticGoals(
            @RequestParam List<String> goals) {

        List<EnhancedVideo> videos = enhancedVideoService.getVideosByTherapeuticGoals(goals);
        return ResponseEntity.ok(videos);
    }

    @GetMapping("/beginner/{moodCategory}")
    public ResponseEntity<List<EnhancedVideo>> getBeginnerVideos(
            @PathVariable String moodCategory) {

        List<EnhancedVideo> videos = enhancedVideoService.getBeginnerFriendlyVideos(moodCategory);
        return ResponseEntity.ok(videos);
    }

    @GetMapping("/quick-help/{moodCategory}")
    public ResponseEntity<List<EnhancedVideo>> getQuickHelpVideos(
            @PathVariable String moodCategory) {

        List<EnhancedVideo> videos = enhancedVideoService.getQuickHelpVideos(moodCategory);
        return ResponseEntity.ok(videos);
    }

    @GetMapping("/content-type/{contentType}")
    public ResponseEntity<List<EnhancedVideo>> getVideosByContentType(
            @PathVariable String contentType,
            @RequestParam String moodCategory) {

        List<EnhancedVideo> videos = enhancedVideoService.getVideosByContentType(contentType, moodCategory);
        return ResponseEntity.ok(videos);
    }

    @GetMapping("/scenario/{scenarioType}")
    public ResponseEntity<List<EnhancedVideo>> getVideosByScenario(
            @PathVariable String scenarioType,
            @RequestParam String moodCategory) {

        List<EnhancedVideo> videos = enhancedVideoService.getScenarioBasedVideos(scenarioType, moodCategory);
        return ResponseEntity.ok(videos);
    }

    @GetMapping("/popular/{moodCategory}")
    public ResponseEntity<List<EnhancedVideo>> getPopularVideos(
            @PathVariable String moodCategory,
            @RequestParam(defaultValue = "10") int limit) {

        List<EnhancedVideo> videos = enhancedVideoService.getPopularVideos(moodCategory, limit);
        return ResponseEntity.ok(videos);
    }

    @PostMapping("/interaction")
    public ResponseEntity<String> recordVideoInteraction(
            @RequestParam String videoId,
            @RequestParam String username,
            @RequestParam String interactionType) {

        enhancedVideoService.recordVideoInteraction(videoId, username, interactionType);
        return ResponseEntity.ok("Interaction recorded successfully");
    }

    @GetMapping("/all")
    public ResponseEntity<List<EnhancedVideo>> getAllActiveVideos() {
        List<EnhancedVideo> videos = enhancedVideoService.getAllActiveVideos();
        return ResponseEntity.ok(videos);
    }

    @GetMapping("/{id}")
    public ResponseEntity<EnhancedVideo> getVideoById(@PathVariable String id) {
        return enhancedVideoService.getVideoById(id)
                .map(video -> ResponseEntity.ok(video))
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<EnhancedVideo> createVideo(@RequestBody EnhancedVideo video) {
        EnhancedVideo savedVideo = enhancedVideoService.saveVideo(video);
        return ResponseEntity.ok(savedVideo);
    }
}
