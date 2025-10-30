package tech.sumithmeena.therascapebackend.config;

import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import tech.sumithmeena.therascapebackend.model.Video;
import tech.sumithmeena.therascapebackend.repository.VideoRepository;

@Configuration
public class DataLoader {
    @Bean
    CommandLineRunner loadSampleVideos(VideoRepository videoRepository) {
        return args -> {
            videoRepository.save(new Video(null, "happy", "https://youtu.be/happy1", "Happy Video 1", "Feel good and smile!"));
            videoRepository.save(new Video(null, "sad", "https://youtu.be/sad1", "Sad Video 1", "It's okay to feel sad."));
            videoRepository.save(new Video(null, "anxious", "https://youtu.be/anxious1", "Anxious Video 1", "Take a deep breath."));
            videoRepository.save(new Video(null, "angry", "https://youtu.be/angry1", "Angry Video 1", "Let go of anger."));
            videoRepository.save(new Video(null, "neutral", "https://youtu.be/neutral1", "Neutral Video 1", "Stay balanced."));
            videoRepository.save(new Video(null, "stressed", "https://youtu.be/stressed1", "Stressed Video 1", "Relax and unwind."));
            videoRepository.save(new Video(null, "depressed", "https://youtu.be/depressed1", "Depressed Video 1", "You are not alone."));
        };
    }
}
