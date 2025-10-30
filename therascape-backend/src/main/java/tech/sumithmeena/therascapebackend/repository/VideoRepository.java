package tech.sumithmeena.therascapebackend.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import tech.sumithmeena.therascapebackend.model.Video;
import java.util.List;

public interface VideoRepository extends MongoRepository<Video, String> {
    List<Video> findByMoodCategoryIgnoreCase(String moodCategory);
}
