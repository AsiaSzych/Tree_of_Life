package com.example.phylo;

import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

public class SimilarityMatrix {
  private final Map<Pair, Integer> matrix = new HashMap<>();

  public void put(String species1, String species2, int score) {
    matrix.put(new Pair(species1, species2), score);
  }

  public Integer get(String species1, String species2) {
    return matrix.get(new Pair(species1, species2));
  }

  public void printAll() {
    for (Map.Entry<Pair, Integer> entry : matrix.entrySet()) {
      System.out.printf("%s - %s: %d%n", entry.getKey().first, entry.getKey().second, entry.getValue());
    }
  }

  public void saveToFile(String filePath) throws IOException {
    Map<String, Integer> exportMap = new HashMap<>();
    for (Map.Entry<Pair, Integer> entry : matrix.entrySet()) {
      String key = entry.getKey().first + "_" + entry.getKey().second;
      exportMap.put(key, entry.getValue());
    }
    ObjectMapper mapper = new ObjectMapper();
    mapper.writerWithDefaultPrettyPrinter().writeValue(new File(filePath), exportMap);
  }

  static class Pair {
    private final String first;
    private final String second;

    public Pair(String first, String second) {
      if (first.compareTo(second) <= 0) {
        this.first = first;
        this.second = second;
      } else {
        this.first = second;
        this.second = first;
      }
    }

    @Override
    public boolean equals(Object o) {
      if (this == o) return true;
      if (o == null || getClass() != o.getClass()) return false;
      Pair pair = (Pair) o;
      return Objects.equals(first, pair.first) && Objects.equals(second, pair.second);
    }

    @Override
    public int hashCode() {
      return Objects.hash(first, second);
    }
  }
}