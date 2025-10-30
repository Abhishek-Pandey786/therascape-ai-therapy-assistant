package tech.sumithmeena.therascapebackend.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;
import org.springframework.stereotype.Repository;
import tech.sumithmeena.therascapebackend.model.EnhancedVideo;

import java.util.List;

@Repository
public interface EnhancedVideoRepository extends MongoRepository<EnhancedVideo, String> {

    // Basic mood-based queries
    List<EnhancedVideo> findByPrimaryMoodCategoryIgnoreCase(String moodCategory);

    List<EnhancedVideo> findBySecondaryMoodCategoriesContainingIgnoreCase(String moodCategory);

    // Intensity-based filtering
    @Query("{ 'primaryMoodCategory': ?0, 'moodIntensityMin': { $lte: ?1 }, 'moodIntensityMax': { $gte: ?1 } }")
    List<EnhancedVideo> findByMoodCategoryAndIntensity(String moodCategory, int intensity);

    // Therapy technique based
    List<EnhancedVideo> findByTherapyTechniqueIgnoreCase(String therapyTechnique);

    // Crisis-safe content
    @Query("{ 'primaryMoodCategory': ?0, 'crisisSafe': true }")
    List<EnhancedVideo> findCrisisSafeByMoodCategory(String moodCategory);

    // Difficulty level filtering
    @Query("{ 'primaryMoodCategory': ?0, 'difficultyLevel': ?1 }")
    List<EnhancedVideo> findByMoodCategoryAndDifficulty(String moodCategory, String difficultyLevel);

    // Content type filtering
    List<EnhancedVideo> findByContentTypeIgnoreCase(String contentType);

    // Scenario type filtering
    List<EnhancedVideo> findByScenarioTypeIgnoreCase(String scenarioType);

    // Duration-based filtering
    @Query("{ 'primaryMoodCategory': ?0, 'durationMinutes': { $lte: ?1 } }")
    List<EnhancedVideo> findByMoodCategoryAndMaxDuration(String moodCategory, int maxDurationMinutes);

    // Comprehensive filtering for personalized recommendations
    @Query("{ " +
            "'primaryMoodCategory': ?0, " +
            "'moodIntensityMin': { $lte: ?1 }, " +
            "'moodIntensityMax': { $gte: ?1 }, " +
            "'crisisSafe': ?2, " +
            "'durationMinutes': { $lte: ?3 }, " +
            "'isActive': true " +
            "}")
    List<EnhancedVideo> findPersonalizedVideos(String moodCategory, int intensity,
            boolean crisisSafe, int maxDuration);

    // Therapeutic goals matching
    @Query("{ 'therapeuticGoals': { $in: ?0 } }")
    List<EnhancedVideo> findByTherapeuticGoalsIn(List<String> goals);

    // Popular videos by mood
    @Query("{ 'primaryMoodCategory': ?0 }")
    List<EnhancedVideo> findPopularByMoodCategory(String moodCategory);

    // Exclude trigger content
    @Query("{ 'primaryMoodCategory': ?0, 'triggers': { $nin: ?1 } }")
    List<EnhancedVideo> findByMoodCategoryExcludingTriggers(String moodCategory, List<String> userTriggers);

    // Find active videos only
    List<EnhancedVideo> findByIsActiveTrueOrderByAverageRatingDesc();
}
