package com.phylogenetic.io;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import java.io.File;
import java.io.IOException;
import java.util.Map;
import java.util.TreeMap;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Handles writing alignment results to JSON files.
 */
public class ResultWriter {
  private static final Logger logger = LoggerFactory.getLogger(ResultWriter.class);
  private final ObjectMapper objectMapper;

  public ResultWriter() {
    this.objectMapper = new ObjectMapper();
    this.objectMapper.enable(SerializationFeature.INDENT_OUTPUT);
  }

  /**
   * Save alignment scores to a JSON file.
   * 
   * @param scoreMatrix The nested map of organism pairs and their scores
   * @param matrixType The BLOSUM matrix type (e.g., "BLOSUM50")
   * @throws IOException if file writing fails
   */
  public void saveScores(Map<String, Map<String, Integer>> scoreMatrix, 
      String matrixType) throws IOException {
    // Extract the number from matrix type (e.g., "BLOSUM50" -> "50")
    String matrixNumber = matrixType.replaceAll("[^0-9]", "");
    String filename = String.format("organisms_scores_blosum%s.json", matrixNumber);
    
    logger.info("Saving alignment scores to file: {}", filename);
    
    // Convert nested map to flat map with concatenated keys
    Map<String, Integer> flatScores = convertToFlatMap(scoreMatrix);
    
    // Write to file
    File outputFile = new File(filename);
    objectMapper.writeValue(outputFile, flatScores);
    
    logger.info("Successfully saved {} alignment scores", flatScores.size());
  }

  /**
   * Convert nested score matrix to flat map with concatenated keys.
   * Only includes unique pairs (avoids duplicates like A_B and B_A).
   */
  private Map<String, Integer> convertToFlatMap(
      Map<String, Map<String, Integer>> scoreMatrix) {
    // Use TreeMap for consistent ordering in output
    Map<String, Integer> flatMap = new TreeMap<>();
    
    for (Map.Entry<String, Map<String, Integer>> outerEntry : scoreMatrix.entrySet()) {
      String organism1 = outerEntry.getKey();
      
      for (Map.Entry<String, Integer> innerEntry : outerEntry.getValue().entrySet()) {
        String organism2 = innerEntry.getKey();
        Integer score = innerEntry.getValue();
        
        // Create key by concatenating organism names
        // Ensure consistent ordering to avoid duplicates
        String key;
        if (organism1.compareTo(organism2) <= 0) {
          key = organism1 + "_" + organism2;
        } else {
          key = organism2 + "_" + organism1;
        }
        
        // Only add if not already present (avoids duplicates)
        if (!flatMap.containsKey(key)) {
          flatMap.put(key, score);
        }
      }
    }
    
    return flatMap;
  }
}