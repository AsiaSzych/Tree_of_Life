package com.phylogenetic.io;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.phylogenetic.model.AlignmentResult;
import java.io.File;
import java.io.IOException;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Handles writing alignment results to JSON files.
 */
public class ResultWriter {
  private final ObjectMapper objectMapper;
  
  public ResultWriter() {
    this.objectMapper = new ObjectMapper();
    this.objectMapper.enable(com.fasterxml.jackson.databind.SerializationFeature.INDENT_OUTPUT);
  }
  
  /**
   * Save alignment results to a JSON file.
   * 
   * @param results List of alignment results
   * @param blosumType The BLOSUM matrix type (e.g., "50" or "62")
   * @throws IOException if file writing fails
   */
  public void saveAlignmentScores(List<AlignmentResult> results, String blosumType) 
      throws IOException {
    // Create the output map with concatenated keys
    Map<String, Integer> scoreMap = new LinkedHashMap<>();
    
    for (AlignmentResult result : results) {
      String key = result.organism1() + "_" + result.organism2();
      scoreMap.put(key, result.score());
    }
    
    // Generate filename based on BLOSUM type
    String filename = "organisms_scores_blosum" + blosumType + ".json";
    File outputFile = new File(filename);
    
    // Write to file
    objectMapper.writeValue(outputFile, scoreMap);
  }
}