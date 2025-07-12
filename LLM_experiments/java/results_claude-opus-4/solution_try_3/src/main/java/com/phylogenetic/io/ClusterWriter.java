package com.phylogenetic.io;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Map;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Writes clustering results to JSON file.
 */
public class ClusterWriter {
  private static final Logger logger = LoggerFactory.getLogger(ClusterWriter.class);
  private final ObjectMapper objectMapper;
  
  public ClusterWriter() {
    this.objectMapper = new ObjectMapper();
    this.objectMapper.enable(SerializationFeature.INDENT_OUTPUT);
  }
  
  /**
   * Save clustering results to JSON file.
   * 
   * @param clusters Map of threshold to list of clusters
   * @param blosumType The BLOSUM matrix type used
   * @throws IOException if file writing fails
   */
  public void saveClusters(Map<Integer, List<List<String>>> clusters, 
      String blosumType) throws IOException {
    String filename = String.format("clusters_for_blosum%s.json", blosumType);
    logger.info("Saving clustering results to file: {}", filename);
    
    File outputFile = new File(filename);
    objectMapper.writeValue(outputFile, clusters);
    
    int totalClusters = clusters.values().stream()
        .mapToInt(List::size)
        .sum();
    
    logger.info("Successfully saved {} thresholds with {} total clusters", 
        clusters.size(), totalClusters);
  }
}