package com.phylogenetic.model;

/**
 * Represents an organism with its amino acid sequence.
 */
public record Organism(String name, String sequence) {
  
  /**
   * Validates the organism data.
   *
   * @throws IllegalArgumentException if name or sequence is null or empty
   */
  public Organism {
    if (name == null || name.isBlank()) {
      throw new IllegalArgumentException("Organism name cannot be null or empty");
    }
    if (sequence == null || sequence.isBlank()) {
      throw new IllegalArgumentException("Organism sequence cannot be null or empty");
    }
  }
}
