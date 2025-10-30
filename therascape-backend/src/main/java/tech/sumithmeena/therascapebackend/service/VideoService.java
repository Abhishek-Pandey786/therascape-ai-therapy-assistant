package tech.sumithmeena.therascapebackend.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import tech.sumithmeena.therascapebackend.model.Video;
import tech.sumithmeena.therascapebackend.repository.VideoRepository;

import java.util.List;

@Service
public class VideoService {
    @Autowired
    private VideoRepository videoRepository;

    public List<Video> getVideosByMoodCategory(String moodCategory) {
        return videoRepository.findByMoodCategoryIgnoreCase(moodCategory);
    }
}
