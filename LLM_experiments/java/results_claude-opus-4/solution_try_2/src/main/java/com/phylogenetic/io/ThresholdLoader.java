package com.phylogenetic.io;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Logger;

/**
 * Loads threshold values from a text file.
 */
public class ThresholdLoader {
  private static final Logger LOGGER = Logger.getLogger(ThresholdLoader.class.getName());
  
  /**
   * Load threshold values from a text file.
   * 
   * @param filename The name of the file containing thresholds
   * @return List of threshold values
   * @throws IOException if file reading fails
   */
  public List<Integer> loadThresholds(String filename) throws IOException {
    List<Integer> thresholds = new ArrayList<>();
    
    try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
      String line;
      int lineNumber = 0;
      
      while ((line = reader.readLine()) != null) {
        lineNumber++;
        line = line.trim();
        
        if (!line.isEmpty()) {
          try {
            int threshold = Integer.parseInt(line);
            thresholds.add(threshold);
          } catch (NumberFormatException e) {
            LOGGER.warning("Invalid threshold value at line " + lineNumber + ": " + line);
          }
        }
      }
    }
    
    LOGGER.info("Loaded " + thresholds.size() + " thresholds from " + filename);
    return thresholds;
  }
}