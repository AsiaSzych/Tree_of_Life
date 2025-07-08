package com.phylogenetic.io;

import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Map;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Handles writing clustering results to JSON files.
 */
public class ClusterWriter {
  private static final Logger logger = LoggerFactory.getLogger(ClusterWriter.class);
  private final ObjectMapper objectMapper;
  
  public ClusterWriter() {
    this.objectMapper = new ObjectMapper();
    this.objectMapper.enable(com.fasterxml.jackson.databind.SerializationFeature.INDENT_OUTPUT);
  }
  
  /**
   * Saves clustering results to a JSON file.
   *
   * @param clusters map of threshold to clusters
   * @param blosumType the BLOSUM matrix type used
   * @throws IOException if file cannot be written
   */
  public void saveClusters(
      Map<Integer, List<List<String>>> clusters, 
      String blosumType) throws IOException {
    
    // Extract the number from BLOSUM type
    String blosumNumber = blosumType.replaceAll("[^0-9]", "");
    String filename = String.format("clusters_for_blosum%s.json", blosumNumber);
    
    logger.info("Saving clustering results to file: {}", filename);
    
    // Write to file
    File outputFile = new File(filename);
    objectMapper.writeValue(outputFile, clusters);
    
    logger.info("Successfully saved {} clustering results to {}", 
        clusters.size(), filename);
  }
}