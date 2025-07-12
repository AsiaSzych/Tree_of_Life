package com.phylogenetic.model;

import java.util.Map;
import java.util.Objects;

/**
 * Represents a BLOSUM substitution matrix for sequence alignment.
 */
public class BlosumMatrix {
  private final Map<String, Integer> scores;
  private final String type;
  
  public BlosumMatrix(Map<String, Integer> scores, String type) {
    this.scores = Map.copyOf(scores);
    this.type = type;
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
  public int getSubstitutionScore(char from, char to) {
    //String key = String.valueOf(from).toLowerCase() + String.valueOf(to).toLowerCase();
    String key = String.valueOf(from) + String.valueOf(to);
    Integer score = scores.get(key);
    if (score == null) {
      throw new IllegalArgumentException(
          "Substitution score not found for: " + from + " -> " + to);
    }
    return score;
  }
  
  public String getType() {
    return type;
  }
}