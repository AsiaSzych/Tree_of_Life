package com.phylo.model;

import java.util.HashMap;
import java.util.Map;

/**
 * Represents a BLOSUM substitution matrix with gap penalties.
 */
public class BlosumMatrix {
    private final Map<String, Integer> scoreMap;
    
    public BlosumMatrix(Map<String, Integer> scoreMap) {
        this.scoreMap = new HashMap<>(scoreMap);
    }

    public int getSubstitutionScore(char a, char b) {
        return scoreMap.getOrDefault("" + a + b, Integer.MIN_VALUE);
    }

    public int getGapPenalty(char c) {
        return scoreMap.getOrDefault(String.valueOf(c), Integer.MIN_VALUE);
    }

    public void validate() throws IllegalArgumentException {
        // Basic validation
        if (scoreMap.isEmpty()) {
            throw new IllegalArgumentException("BLOSUM matrix cannot be empty");
        }
    }
}