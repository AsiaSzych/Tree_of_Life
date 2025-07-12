package com.phylogenetic.config;

/**
 * Configuration class for the application.
 */
public class ApplicationConfig {
  private final String organismsFile;
  private final String blosumFile;
  
  public ApplicationConfig(String organismsFile, String blosumFile) {
    this.organismsFile = organismsFile;
    this.blosumFile = blosumFile;
  }
  
  public String getOrganismsFile() {
    return organismsFile;
  }
  
  public String getBlosumFile() {
    return blosumFile;
  }
  
  /**
   * Create default configuration.
   */
  public static ApplicationConfig createDefault(String blosumType) {
    return new ApplicationConfig("organisms.json", "blosum" + blosumType + ".json");
  }
}