package com.phylo.model;

import java.util.Map;

/**
 * Represents BLOSUM substitution matrix with gap penalties.
 */
public class BlosumMatrix {
    private final Map<String, Integer> scoreMap;
    private final int defaultGapPenalty;

    public BlosumMatrix(Map<String, Integer> scoreMap, int defaultGapPenalty) {
        this.scoreMap = Map.copyOf(scoreMap);
        this.defaultGapPenalty = defaultGapPenalty;
    }

    public int getMatchScore(char a, char b) {
        if (a == b) {
            return scoreMap.getOrDefault("" + a + b, defaultGapPenalty);
        }
        return scoreMap.getOrDefault("" + a + b, 
               scoreMap.getOrDefault("" + b + a, defaultGapPenalty));
    }

    public int getGapPenalty(char c) {
        return scoreMap.getOrDefault(String.valueOf(c), defaultGapPenalty);
    }
}