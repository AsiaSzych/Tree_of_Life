package com.phylogenetic.model;

/**
 * Represents the result of a sequence alignment between two organisms.
 */
public record AlignmentResult(
    String organism1,
    String organism2,
    int score) {
  
  /**
   * Creates a symmetric pair key for consistent storage and retrieval.
   *
   * @return a key that is the same regardless of organism order
   */
  public String getPairKey() {
    return organism1.compareTo(organism2) < 0
        ? organism1 + "|" + organism2
        : organism2 + "|" + organism1;
  }
}