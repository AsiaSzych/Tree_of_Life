package com.phylogenetic.model;

/**
 * Represents the result of a sequence alignment between two organisms.
 */
public record AlignmentResult(
    String organism1,
    String organism2,
    int score) {
  
  public AlignmentResult {
    if (organism1 == null || organism2 == null) {
      throw new IllegalArgumentException("Organism names cannot be null");
    }
  }
}