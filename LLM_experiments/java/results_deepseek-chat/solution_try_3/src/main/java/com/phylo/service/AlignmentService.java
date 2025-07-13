package com.phylo.service;

import com.phylo.model.*;
import com.phylo.util.Pair;

import java.util.HashMap;
import java.util.Map;

/**
 * Implements Needleman-Wunsch alignment algorithm.
 */
public class AlignmentService {
    private final BlosumMatrix matrix;
    private final Map<Pair<String>, Integer> scoreCache;

    public AlignmentService(BlosumMatrix matrix) {
        this.matrix = matrix;
        this.scoreCache = new HashMap<>();
    }

    public int calculateAlignmentScore(String seq1, String seq2) {
        int m = seq1.length();
        int n = seq2.length();
        int[][] dp = new int[m + 1][n + 1];

        // Initialize first row and column with gap penalties
        for (int i = 1; i <= m; i++) {
            dp[i][0] = dp[i - 1][0] + matrix.getGapPenalty(seq1.charAt(i - 1));
        }
        for (int j = 1; j <= n; j++) {
            dp[0][j] = dp[0][j - 1] + matrix.getGapPenalty(seq2.charAt(j - 1));
        }

        // Fill DP table
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                char a = seq1.charAt(i - 1);
                char b = seq2.charAt(j - 1);

                int match = dp[i - 1][j - 1] + matrix.getSubstitutionScore(a, b);
                int delete = dp[i - 1][j] + matrix.getGapPenalty(a);
                int insert = dp[i][j - 1] + matrix.getGapPenalty(b);

                dp[i][j] = Math.max(match, Math.max(delete, insert));
            }
        }

        return dp[m][n];
    }

    public Map<Pair<String>, Integer> calculateAllPairs(OrganismData data) {
        Map<Pair<String>, Integer> results = new HashMap<>();
        var species = data.speciesToSequence().keySet().stream().toList();

        for (int i = 0; i < species.size(); i++) {
            for (int j = i; j < species.size(); j++) {
                String species1 = species.get(i);
                String species2 = species.get(j);
                String seq1 = data.speciesToSequence().get(species1);
                String seq2 = data.speciesToSequence().get(species2);

                int score = calculateAlignmentScore(seq1, seq2);
                results.put(new Pair<>(species1, species2), score);
                if (!species1.equals(species2)) {
                    results.put(new Pair<>(species2, species1), score);
                }
            }
        }

        return results;
    }
}
