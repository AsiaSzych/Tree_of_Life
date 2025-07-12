package com.phylogenetic.io;

import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.logging.Logger;

/**
 * Handles writing clustering results to JSON files.
 */
public class ClusterWriter {
  private static final Logger LOGGER = Logger.getLogger(ClusterWriter.class.getName());
  
  private final ObjectMapper objectMapper;
  
  public ClusterWriter() {
    this.objectMapper = new ObjectMapper();
    this.objectMapper.enable(com.fasterxml.jackson.databind.SerializationFeature.INDENT_OUTPUT);
  }
  
  /**
   * Save clustering results to a JSON file.
   * 
   * @param results Map of threshold to clusters
   * @param blosumType The BLOSUM matrix type used
   * @throws IOException if file writing fails
   */
  public void saveClusteringResults(Map<Integer, List<List<String>>> results, 
                                    String blosumType) throws IOException {
    // Use TreeMap to ensure consistent ordering by threshold
    Map<Integer, List<List<String>>> sortedResults = new TreeMap<>(results);
    
    String filename = "clusters_for_blosum" + blosumType + ".json";
    File outputFile = new File(filename);
    
    objectMapper.writeValue(outputFile, sortedResults);
    
    LOGGER.info("Saved clustering results to " + filename);
  }
}