package com.phylogenetic.io;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Loads similarity scores from JSON files.
 */
public class ScoreLoader {
  private static final Logger logger = LoggerFactory.getLogger(ScoreLoader.class);
  private final ObjectMapper objectMapper;
  
  public ScoreLoader() {
    this.objectMapper = new ObjectMapper();
  }
  
  /**
   * Load scores from flat JSON format and convert to nested map.
   */
  public Map<String, Map<String, Integer>> loadScores(String filename) 
      throws IOException {
    logger.info("Loading scores from file: {}", filename);
    File file = new File(filename);
    
    Map<String, Integer> flatScores = objectMapper.readValue(
        file, new TypeReference<Map<String, Integer>>() {});
    
    // Convert flat map to nested map
    Map<String, Map<String, Integer>> scoreMatrix = new HashMap<>();
    
    for (Map.Entry<String, Integer> entry : flatScores.entrySet()) {
      String key = entry.getKey();
      Integer score = entry.getValue();
      
      // Split key into two species names
      String[] parts = key.split("_", 2);
      if (parts.length == 2) {
        String species1 = parts[0];
        String species2 = parts[1];
        
        // Add to matrix in both directions
        scoreMatrix.computeIfAbsent(species1, k -> new HashMap<>())
            .put(species2, score);
        scoreMatrix.computeIfAbsent(species2, k -> new HashMap<>())
            .put(species1, score);
      }
    }
    
    logger.info("Loaded scores for {} species", scoreMatrix.size());
    return scoreMatrix;
  }
}
