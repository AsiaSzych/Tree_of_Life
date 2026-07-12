package com.phylogenetic.model;

import java.util.HashMap;
import java.util.Map;

/**
 * Represents a BLOSUM substitution matrix for sequence alignment.
 */
public class BlosumMatrix {
  private final Map<String, Integer> scores;
  private final String matrixType;
  
  public BlosumMatrix(Map<String, Integer> scores, String matrixType) {
    this.scores = new HashMap<>(scores);
    this.matrixType = matrixType;
  }
  
  /**
   * Gets the gap penalty for inserting/deleting a character.
   *
   * @param aminoAcid the amino acid character
   * @return the gap penalty (negative value)
   */
  public int getGapPenalty(char aminoAcid) {
    String key = String.valueOf(aminoAcid); //.toLowerCase();
    Integer penalty = scores.get(key);
    if (penalty == null) {
      throw new IllegalArgumentException(
          "Gap penalty not found for amino acid: " + aminoAcid);
    }
    return penalty;
  }
  
  /**
   * Gets the substitution score between two amino acids.
   *
   * @param from first amino acid
   * @param to second amino acid
   * @return the substitution score
   */
  public int getSubstitutionScore(char from, char to) {
    String key = String.valueOf(from) + String.valueOf(to);
    Integer score = scores.get(key);
    if (score == null) {
      throw new IllegalArgumentException(
          "Substitution score not found for: " + from + " -> " + to);
    }
    return score;
  }
  
  public String getMatrixType() {
    return matrixType;
  }
}