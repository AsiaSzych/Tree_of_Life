package com.phylogenetic.model;

/**
 * Represents the result of sequence alignment between two organisms.
 */
public record AlignmentResult(
    String organism1,
    String organism2,
    int score) implements Comparable<AlignmentResult> {

  @Override
  public int compareTo(AlignmentResult other) {
    // Sort by organism names for consistent ordering
    int cmp = organism1.compareTo(other.organism1);
    if (cmp != 0) return cmp;
    return organism2.compareTo(other.organism2);
  }
}