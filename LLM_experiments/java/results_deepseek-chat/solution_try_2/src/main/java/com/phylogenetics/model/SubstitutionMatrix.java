package com.phylogenetics.model;

import java.util.HashMap;
import java.util.Map;

/**
 * Represents a BLOSUM substitution matrix for sequence alignment.
 */
public class SubstitutionMatrix {
    private final Map<String, Integer> scores;
    private final int gapPenalty;

    public SubstitutionMatrix(Map<String, Integer> scores) {
        this.scores = new HashMap<>(scores);
        // Default gap penalty if not specified in the matrix
        this.gapPenalty = scores.getOrDefault("-", -1);
    }

    public int getScore(char a, char b) {
        String key = String.valueOf(a) + b;
        return scores.getOrDefault(key, scores.getOrDefault(Character.toString(a), gapPenalty));
    }

    public int getGapPenalty() {
        return gapPenalty;
    }
}