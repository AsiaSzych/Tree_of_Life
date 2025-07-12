package com.phylogenetic.model;

import java.util.Map;
import java.util.Objects;

/**
 * Represents a BLOSUM substitution matrix for sequence alignment.
 */
public class BlosumMatrix {
  private final Map<String, Integer> scores;
  private final String matrixType;

  public BlosumMatrix(Map<String, Integer> scores, String matrixType) {
    this.scores = Map.copyOf(Objects.requireNonNull(scores, "Scores map cannot be null"));
    this.matrixType = Objects.requireNonNull(matrixType, "Matrix type cannot be null");
  }

  /**
   * Get the gap penalty for a specific amino acid.
   */
  public int getGapPenalty(char aminoAcid) {
    String key = String.valueOf(aminoAcid);//.toLowerCase();
    Integer penalty = scores.get(key);
    if (penalty == null) {
      throw new IllegalArgumentException(
          "Gap penalty not found for amino acid: " + aminoAcid);
    }
    return penalty;
  }

  /**
   * Get the substitution score between two amino acids.
   */
  public int getSubstitutionScore(char aminoAcid1, char aminoAcid2) {
    // String key = String.valueOf(aminoAcid1).toLowerCase() 
    //     + String.valueOf(aminoAcid2).toLowerCase();
    String key = String.valueOf(aminoAcid1) 
        + String.valueOf(aminoAcid2);
    Integer score = scores.get(key);
    if (score == null) {
      throw new IllegalArgumentException(
          "Substitution score not found for pair: " + aminoAcid1 + ", " + aminoAcid2);
    }
    return score;
  }

  public String getMatrixType() {
    return matrixType;
  }
}