package com.example.phylo;

import java.util.HashMap;
import java.util.Map;

public class BlosumMatrix {
    private final Map<String, Integer> substitutionScores;
    private final Map<Character, Integer> deletionScores;

    public BlosumMatrix(Map<String, Integer> rawScores) {
        this.substitutionScores = new HashMap<>();
        this.deletionScores = new HashMap<>();
        for (Map.Entry<String, Integer> entry : rawScores.entrySet()) {
            String key = entry.getKey();
            Integer value = entry.getValue();
            if (key.length() == 1) {
                deletionScores.put(key.charAt(0), value);
            } else if (key.length() == 2) {
                substitutionScores.put(key, value);
            }
        }
    }

    public int getSubstitutionScore(char a, char b) {
        String key = "" + a + b;
        return substitutionScores.getOrDefault(key, Integer.MIN_VALUE);
    }

    public int getDeletionScore(char a) {
        return deletionScores.getOrDefault(a, Integer.MIN_VALUE);
    }
}