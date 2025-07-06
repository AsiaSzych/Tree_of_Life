package com.phylo;

import java.util.List;
import java.util.Map;
import java.util.ArrayList;
import java.util.HashMap;

public class NeedlemanWunschScorer {
    private final Map<Character, Integer> deletionCostMap;
    private final Map<String, Integer> substitutionMap;

    public NeedlemanWunschScorer(Map<String, Integer> blosumMap) {
        this.deletionCostMap = new HashMap<>();
        this.substitutionMap = new HashMap<>();
        processBlosumMap(blosumMap);
    }

    private void processBlosumMap(Map<String, Integer> blosumMap) {
        for (Map.Entry<String, Integer> entry : blosumMap.entrySet()) {
            String key = entry.getKey().toUpperCase();
            if (key.length() == 1) {
                deletionCostMap.put(key.charAt(0), entry.getValue());
            } else if (key.length() == 2) {
                substitutionMap.put(key, entry.getValue());
            }
        }
    }

    public int computeScore(String seq1, String seq2) {
        validateSequence(seq1);
        validateSequence(seq2);
        int m = seq1.length();
        int n = seq2.length();
        int[][] dp = new int[m + 1][n + 1];

        // Initialize first row and column
        for (int i = 1; i <= m; i++) {
            dp[i][0] = dp[i - 1][0] + deletionCostMap.get(seq1.charAt(i - 1));
        }
        for (int j = 1; j <= n; j++) {
            dp[0][j] = dp[0][j - 1] + deletionCostMap.get(seq2.charAt(j - 1));
        }

        // Fill DP table
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                char a = seq1.charAt(i - 1);
                char b = seq2.charAt(j - 1);
                int matchScore = dp[i - 1][j - 1] + getSubstitutionScore(a, b);
                int gapInSeq1 = dp[i - 1][j] + deletionCostMap.get(a);
                int gapInSeq2 = dp[i][j - 1] + deletionCostMap.get(b);
                dp[i][j] = Math.max(Math.max(matchScore, gapInSeq1), gapInSeq2);
            }
        }
        return dp[m][n];
    }

    private int getSubstitutionScore(char a, char b) {
        String key1 = String.valueOf(a) + b;
        String key2 = String.valueOf(b) + a;
        if (substitutionMap.containsKey(key1)) {
            return substitutionMap.get(key1);
        } else if (substitutionMap.containsKey(key2)) {
            return substitutionMap.get(key2);
        } else {
            throw new IllegalArgumentException(
                "Missing substitution score for pair: " + a + " and " + b
            );
        }
    }

    private void validateSequence(String sequence) {
        for (char c : sequence.toCharArray()) {
            if (!deletionCostMap.containsKey(c)) {
                throw new IllegalArgumentException(
                    "Residue '" + c + "' not found in BLOSUM deletion costs"
                );
            }
        }
    }
}