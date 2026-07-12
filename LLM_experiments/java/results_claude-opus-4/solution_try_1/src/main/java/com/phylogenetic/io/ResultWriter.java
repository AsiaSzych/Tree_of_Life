package com.phylogenetic.io;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.phylogenetic.model.AlignmentResult;
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
    this.objectMapper.enable(com.fasterxml.jackson.databind.SerializationFeature.INDENT_OUTPUT);
  }
  
  /**
   * Saves alignment results to a JSON file.
   *
   * @param results map of alignment results
   * @param matrixType the BLOSUM matrix type used (e.g., "BLOSUM50", "BLOSUM62")
   * @throws IOException if file cannot be written
   */
  public void saveResults(Map<String, AlignmentResult> results, String matrixType) 
      throws IOException {
    // Extract the number from matrix type (e.g., "BLOSUM62" -> "62")
    String matrixNumber = matrixType.replaceAll("[^0-9]", "");
    String filename = String.format("organisms_scores_blosum%s.json", matrixNumber);
    
    logger.info("Saving alignment results to file: {}", filename);
    
    // Convert results to the required format
    Map<String, Integer> formattedResults = new TreeMap<>(); // TreeMap for sorted output
    for (AlignmentResult result : results.values()) {
      String key = result.organism1() + "_" + result.organism2();
      formattedResults.put(key, result.score());
    }
    
    // Write to file
    File outputFile = new File(filename);
    objectMapper.writeValue(outputFile, formattedResults);
    
    logger.info("Successfully saved {} alignment scores to {}", 
        formattedResults.size(), filename);
  }
}