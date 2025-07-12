package com.phylogenetic.io;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.phylogenetic.model.BlosumMatrix;
import com.phylogenetic.model.Organism;
import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * Handles loading data from JSON files.
 */
public class DataLoader {
  private final ObjectMapper objectMapper;
  
  public DataLoader() {
    this.objectMapper = new ObjectMapper();
  }
  
  /**
   * Load organisms from JSON file.
   */
  public List<Organism> loadOrganisms(String filename) throws IOException {
    File file = new File(filename);
    Map<String, String> data = objectMapper.readValue(
        file, new TypeReference<Map<String, String>>() {});
    
    return data.entrySet().stream()
        .map(entry -> new Organism(entry.getKey(), entry.getValue()))
        .collect(Collectors.toList());
  }
  
  /**
   * Load BLOSUM matrix from JSON file.
   */
  public BlosumMatrix loadBlosumMatrix(String filename) throws IOException {
    File file = new File(filename);
    Map<String, Integer> scores = objectMapper.readValue(
        file, new TypeReference<Map<String, Integer>>() {});
    
    // Extract type from filename (e.g., "blosum50.json" -> "50")
    String type = filename.replaceAll(".*blosum(\\d+)\\.json", "$1");
    
    return new BlosumMatrix(scores, type);
  }
}