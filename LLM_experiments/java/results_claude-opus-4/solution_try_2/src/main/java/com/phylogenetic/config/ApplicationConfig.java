package com.phylogenetic.config;

/**
 * Configuration constants for the application.
 */
public final class ApplicationConfig {
  private ApplicationConfig() {
    // Prevent instantiation
  }
  
  public static final String DEFAULT_ORGANISMS_FILE = "organisms.json";
  public static final String DEFAULT_BLOSUM_FILE = "blosum62.json";
  public static final String SCORES_FILE_PREFIX = "organisms_scores_blosum";
  public static final String SCORES_FILE_SUFFIX = ".json";
  
  /**
   * Generate the output filename for alignment scores.
   */
  public static String getScoresFilename(String blosumType) {
    return SCORES_FILE_PREFIX + blosumType + SCORES_FILE_SUFFIX;
  }
}