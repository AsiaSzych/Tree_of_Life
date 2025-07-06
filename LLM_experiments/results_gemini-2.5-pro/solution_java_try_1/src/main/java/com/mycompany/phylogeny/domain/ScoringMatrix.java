package com.mycompany.phylogeny.domain;

import java.util.Map;
import java.util.Objects;

/**
 * Represents the scoring matrix (e.g., BLOSUM) for sequence alignment.
 * This class provides a clean interface to get substitution scores and gap penalties,
 * abstracting the underlying map-based storage.
 */
public class ScoringMatrix {

  private final Map<String, Integer> scores;

  public ScoringMatrix(Map<String, Integer> scores) {
    this.scores = Objects.requireNonNull(scores, "Scores map cannot be null.");
  }

  /**
   * Gets the substitution score between two amino acid characters.
   *
   * @param a The first character.
   * @param b The second character.
   * @return The substitution score.
   * @throws IllegalArgumentException if the score for the given pair is not found.
   */
  public int getSubstitutionScore(char a, char b) {
    // Keys are stored as sorted character pairs to handle both "AG" and "GA"
    String key = (a < b) ? "" + a + b : "" + b + a;
    return scores.getOrDefault(key, scores.get("" + a + b));
  }

  /**
   * Gets the gap penalty for a specific amino acid character.
   *
   * @param c The character being aligned with a gap.
   * @return The gap penalty score.
   * @throws IllegalArgumentException if the gap penalty for the character is not found.
   */
  public int getGapPenalty(char c) {
    return scores.get(String.valueOf(c));
  }
}