package com.phylogenetic.model;

/**
 * Represents an organism with its amino acid sequence.
 */
public record Organism(String name, String sequence) {
  
  public Organism {
    if (name == null || name.isBlank()) {
      throw new IllegalArgumentException("Organism name cannot be null or blank");
    }
    if (sequence == null || sequence.isBlank()) {
      throw new IllegalArgumentException("Organism sequence cannot be null or blank");
    }
  }
}