package com.example.phylo;

import java.util.Map;

public class BlosumMatrix {

  private final Map<String, Integer> matrix;

  public BlosumMatrix(Map<String, Integer> matrix) {
    this.matrix = matrix;
  }

  public int getSubstitutionScore(char a, char b) {
    String key = "" + a + b;
    Integer score = matrix.get(key);
    if (score == null) {
      throw new IllegalArgumentException("No substitution score for pair: " + key);
    }
    return score;
  }

  public int getDeletionScore(char a) {
    String key = "" + a;
    Integer score = matrix.get(key);
    if (score == null) {
      throw new IllegalArgumentException("No deletion score for: " + key);
    }
    return score;
  }
}