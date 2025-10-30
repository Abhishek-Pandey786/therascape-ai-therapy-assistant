package tech.sumithmeena.therascapebackend.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import tech.sumithmeena.therascapebackend.model.Video;
import tech.sumithmeena.therascapebackend.service.VideoService;

import java.util.List;

@RestController
@RequestMapping("/api/videos")
public class VideoController {
    @Autowired
    private VideoService videoService;

    @GetMapping("/mood/{category}")
    public List<Video> getVideosByMood(@PathVariable String category) {
        return videoService.getVideosByMoodCategory(category);
    }
}
