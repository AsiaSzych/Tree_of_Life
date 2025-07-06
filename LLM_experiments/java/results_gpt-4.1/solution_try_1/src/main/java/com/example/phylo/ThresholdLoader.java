package com.example.phylo;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

public class ThresholdLoader {
  public static ArrayList<Integer> loadThresholds(String filePath) throws IOException {
    ArrayList<Integer> thresholds = new ArrayList<>();
    try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
      String line;
      while ((line = br.readLine()) != null) {
        line = line.trim();
        if (!line.isEmpty()) {
          thresholds.add(Integer.parseInt(line));
        }
      }
    }
    return thresholds;
  }
}
