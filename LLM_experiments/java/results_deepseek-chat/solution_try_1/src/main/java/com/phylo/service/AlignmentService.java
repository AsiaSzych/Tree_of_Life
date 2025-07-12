package com.phylo.service;

import com.phylo.model.BlosumMatrix;
import com.phylo.util.Pair;
import com.phylo.model.Organisms;
import java.util.HashMap;
import java.util.Map;
import java.io.IOException;

/**
 * Implements Needleman-Wunsch alignment algorithm.
 */
public class AlignmentService {
    private final BlosumMatrix blosumMatrix;
    private final Map<Pair<String>, Integer> scoreCache = new HashMap<>();

    public AlignmentService(BlosumMatrix blosumMatrix) {
        this.blosumMatrix = blosumMatrix;
    }

    public int calculateAlignmentScore(String seq1, String seq2) {
        int m = seq1.length();
        int n = seq2.length();
        int[][] dp = new int[m + 1][n + 1];

        // Initialize first row and column with gap penalties
        for (int i = 1; i <= m; i++) {
            dp[i][0] = dp[i-1][0] + blosumMatrix.getGapPenalty(seq1.charAt(i-1));
        }
        for (int j = 1; j <= n; j++) {
            dp[0][j] = dp[0][j-1] + blosumMatrix.getGapPenalty(seq2.charAt(j-1));
        }

        // Fill DP table
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                char a = seq1.charAt(i-1);
                char b = seq2.charAt(j-1);

                int match = dp[i-1][j-1] + blosumMatrix.getMatchScore(a, b);
                int delete = dp[i-1][j] + blosumMatrix.getGapPenalty(a);
                int insert = dp[i][j-1] + blosumMatrix.getGapPenalty(b);

                dp[i][j] = Math.max(Math.max(match, delete), insert);
            }
        }

        return dp[m][n];
    }

    public Map<Pair<String>, Integer> calculateAllPairs(Organisms organisms) {
        Map<Pair<String>, Integer> scores = new HashMap<>();
        var species = organisms.speciesMap().keySet().stream().toList();

        for (int i = 0; i < species.size(); i++) {
            for (int j = i; j < species.size(); j++) {
                String species1 = species.get(i);
                String species2 = species.get(j);
                String seq1 = organisms.getSequence(species1);
                String seq2 = organisms.getSequence(species2);

                int score = calculateAlignmentScore(seq1, seq2);
                scores.put(new Pair<>(species1, species2), score);
                if (!species1.equals(species2)) {
                    scores.put(new Pair<>(species2, species1), score);
                }
            }
        }

        scoreCache.putAll(scores);
        return scores;
    }

    public Map<String, Integer> calculateAndSaveAllPairs(
            Organisms organisms, 
            String blosumType) throws IOException {
        Map<Pair<String>, Integer> pairScores = calculateAllPairs(organisms);
        Map<String, Integer> formattedScores = new HashMap<>();
        
        pairScores.forEach((pair, score) -> {
            String key = pair.first() + "_" + pair.second();
            formattedScores.put(key, score);
        });

        FileService.saveScoresToFile(formattedScores, blosumType);
        return formattedScores;
    }
}