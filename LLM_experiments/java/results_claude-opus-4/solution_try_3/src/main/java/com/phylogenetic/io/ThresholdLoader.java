package com.phylogenetic.io;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Loads threshold values from text file.
 */
public class ThresholdLoader {
  private static final Logger logger = LoggerFactory.getLogger(ThresholdLoader.class);
  
  /**
   * Load threshold values from file.
   * 
   * @param filename The file to read from
   * @return List of threshold values
   * @throws IOException if file reading fails
   */
  public List<Integer> loadThresholds(String filename) throws IOException {
    logger.info("Loading thresholds from file: {}", filename);
    List<Integer> thresholds = new ArrayList<>();
    
    try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
      String line;
      int lineNumber = 0;
      
      while ((line = reader.readLine()) != null) {
        lineNumber++;
        line = line.trim();
        
        if (line.isEmpty()) {
          continue; // Skip empty lines
        }
        
        try {
          int threshold = Integer.parseInt(line);
          thresholds.add(threshold);
          logger.debug("Loaded threshold: {}", threshold);
        } catch (NumberFormatException e) {
          logger.warn("Invalid threshold at line {}: '{}' - skipping", 
              lineNumber, line);
        }
      }
    }
    
    logger.info("Loaded {} thresholds", thresholds.size());
    return thresholds;
  }
}