package com.example.phylo;

import java.util.Map;

public class BlosumMatrix {
  private final Map<String, Integer> matrix;

  public BlosumMatrix(Map<String, Integer> matrix) {
    this.matrix = matrix;
  }

  public int getSubstitutionScore(char a, char b) {
    String key = "" + a + b;
    return matrix.getOrDefault(key, Integer.MIN_VALUE);
  }

  public int getDeletionScore(char a) {
    String key = "" + a;
    return matrix.getOrDefault(key, Integer.MIN_VALUE);
  }
}