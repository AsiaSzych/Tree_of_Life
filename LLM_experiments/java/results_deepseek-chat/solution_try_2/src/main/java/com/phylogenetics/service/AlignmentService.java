package com.phylogenetics.service;

import com.phylogenetics.model.Organism;
import com.phylogenetics.model.SubstitutionMatrix;

import java.util.HashMap;
import java.util.Map;

/**
 * Implements the Needleman-Wunsch algorithm for global sequence alignment.
 */
public class AlignmentService {
    private final SubstitutionMatrix matrix;

    public AlignmentService(SubstitutionMatrix matrix) {
        this.matrix = matrix;
    }

    public Map<String, Map<String, Integer>> calculateAllPairs(Map<String, Organism> organisms) {
        Map<String, Map<String, Integer>> scores = new HashMap<>();
        
        organisms.values().forEach(org1 -> {
            Map<String, Integer> row = new HashMap<>();
            organisms.values().forEach(org2 -> {
                row.put(org2.name(), align(org1.sequence(), org2.sequence()));
            });
            scores.put(org1.name(), row);
        });
        
        return scores;
    }

    public int align(String seq1, String seq2) {
        int m = seq1.length();
        int n = seq2.length();
        
        int[][] dp = new int[m + 1][n + 1];
        
        // Initialize first row and column with gap penalties
        for (int i = 0; i <= m; i++) {
            dp[i][0] = i * matrix.getGapPenalty();
        }
        for (int j = 0; j <= n; j++) {
            dp[0][j] = j * matrix.getGapPenalty();
        }
        
        // Fill the DP matrix
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                char a = seq1.charAt(i - 1);
                char b = seq2.charAt(j - 1);
                
                int match = dp[i - 1][j - 1] + matrix.getScore(a, b);
                int delete = dp[i - 1][j] + matrix.getGapPenalty();
                int insert = dp[i][j - 1] + matrix.getGapPenalty();
                
                dp[i][j] = Math.max(match, Math.max(delete, insert));
            }
        }
        
        return dp[m][n];
    }
}