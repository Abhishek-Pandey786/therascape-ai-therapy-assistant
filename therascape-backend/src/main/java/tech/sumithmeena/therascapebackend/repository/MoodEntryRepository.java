package tech.sumithmeena.therascapebackend.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;
import org.springframework.stereotype.Repository;
import tech.sumithmeena.therascapebackend.model.MoodEntry;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface MoodEntryRepository extends MongoRepository<MoodEntry, String> {

    List<MoodEntry> findByUserIdOrderByTimestampDesc(String userId);

    List<MoodEntry> findByUserIdAndTimestampBetweenOrderByTimestampDesc(
            String userId, LocalDateTime start, LocalDateTime end);

    @Query("{ 'userId': ?0, 'crisisRisk': true }")
    List<MoodEntry> findCrisisEntriesByUserId(String userId);

    @Query(value = "{ 'userId': ?0, 'timestamp': { '$gte': ?1 } }", fields = "{ 'intensity': 1 }")
    List<MoodEntry> findIntensityByUserIdSince(String userId, LocalDateTime since);

    @Query("{ 'userId': ?0 }")
    List<MoodEntry> findByUserId(String userId);

    List<MoodEntry> findTop10ByUserIdOrderByTimestampDesc(String userId);

    long countByUserIdAndCrisisRisk(String userId, boolean crisisRisk);
}
