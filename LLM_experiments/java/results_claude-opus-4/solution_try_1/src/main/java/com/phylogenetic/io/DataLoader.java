package com.phylogenetic.io;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.phylogenetic.model.BlosumMatrix;
import com.phylogenetic.model.Organism;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Handles loading data from JSON files.
 */
public class DataLoader {
  private static final Logger logger = LoggerFactory.getLogger(DataLoader.class);
  private final ObjectMapper objectMapper = new ObjectMapper();
  
  /**
   * Loads organisms from a JSON file.
   *
   * @param filename the name of the file to load
   * @return list of organisms
   * @throws IOException if file cannot be read
   */
  public List<Organism> loadOrganisms(String filename) throws IOException {
    logger.info("Loading organisms from file: {}", filename);
    File file = new File(filename);
    
    Map<String, String> organismsMap = objectMapper.readValue(
        file, new TypeReference<Map<String, String>>() {});
    
    List<Organism> organisms = new ArrayList<>();
    for (Map.Entry<String, String> entry : organismsMap.entrySet()) {
      organisms.add(new Organism(entry.getKey(), entry.getValue()));
    }
    
    logger.info("Loaded {} organisms", organisms.size());
    return organisms;
  }
  
  /**
   * Loads a BLOSUM matrix from a JSON file.
   *
   * @param filename the name of the file to load
   * @return the BLOSUM matrix
   * @throws IOException if file cannot be read
   */
  public BlosumMatrix loadBlosumMatrix(String filename) throws IOException {
    logger.info("Loading BLOSUM matrix from file: {}", filename);
    File file = new File(filename);
    
    Map<String, Integer> scores = objectMapper.readValue(
        file, new TypeReference<Map<String, Integer>>() {});
    
    // Extract matrix type from filename (e.g., "blosum50.json" -> "BLOSUM50")
    String matrixType = filename.substring(0, filename.lastIndexOf('.'))
        .toUpperCase();
    
    logger.info("Loaded {} matrix with {} entries", matrixType, scores.size());
    return new BlosumMatrix(scores, matrixType);
  }
}
