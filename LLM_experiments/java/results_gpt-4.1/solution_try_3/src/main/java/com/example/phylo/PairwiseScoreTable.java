package com.example.phylo;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;

public class PairwiseScoreTable {

  private final Map<String, Map<String, Integer>> scoreTable = new HashMap<>();

  public void put(String speciesA, String speciesB, int score) {
    scoreTable.computeIfAbsent(speciesA, k -> new HashMap<>()).put(speciesB, score);
    scoreTable.computeIfAbsent(speciesB, k -> new HashMap<>()).put(speciesA, score);
  }

  public Integer get(String speciesA, String speciesB) {
    Map<String, Integer> inner = scoreTable.get(speciesA);
    if (inner != null) {
      return inner.get(speciesB);
    }
    return null;
  }

  public Set<String> getSpecies() {
    return scoreTable.keySet();
  }

  public Map<String, Integer> getScoresFor(String species) {
    return scoreTable.get(species);
  }

  public Map<String, Integer> toFlatMap() {
    Map<String, Integer> flatMap = new HashMap<>();
    for (String speciesA : scoreTable.keySet()) {
      for (Map.Entry<String, Integer> entry : scoreTable.get(speciesA).entrySet()) {
        String speciesB = entry.getKey();
        if (speciesA.compareTo(speciesB) < 0) {
          String key = speciesA + "_" + speciesB;
          flatMap.put(key, entry.getValue());
        }
      }
    }
    return flatMap;
  }
}