package com.phylogen.service;

import com.phylogen.model.ScoringMatrix;

/**
 * Implements the Needleman-Wunsch algorithm to find the optimal global alignment score.
 */
public class NeedlemanWunschAligner {

    private final ScoringMatrix scoringMatrix;

    public NeedlemanWunschAligner(ScoringMatrix scoringMatrix) {
        this.scoringMatrix = scoringMatrix;
    }

    /**
     * Calculates the alignment score for two DNA sequences.
     *
     * @param seq1 The first sequence.
     * @param seq2 The second sequence.
     * @return The optimal alignment score as an integer.
     */
    public int calculateScore(String seq1, String seq2) {
        int len1 = seq1.length();
        int len2 = seq2.length();

        // DP table to store scores
        int[][] dp = new int[len1 + 1][len2 + 1];

        // Initialize the DP table
        // First column (aligning seq1 with gaps)
        for (int i = 1; i <= len1; i++) {
            dp[i][0] = dp[i - 1][0] + scoringMatrix.getGapPenalty(seq1.charAt(i - 1));
        }
        // First row (aligning seq2 with gaps)
        for (int j = 1; j <= len2; j++) {
            dp[0][j] = dp[0][j - 1] + scoringMatrix.getGapPenalty(seq2.charAt(j - 1));
        }

        // Fill the rest of the table
        for (int i = 1; i <= len1; i++) {
            for (int j = 1; j <= len2; j++) {
                char char1 = seq1.charAt(i - 1);
                char char2 = seq2.charAt(j - 1);

                // Score for matching/mismatching the current characters
                int matchScore = dp[i - 1][j - 1] + scoringMatrix.getSubstitutionScore(char1, char2);
                // Score for deleting a character from seq1 (aligning with a gap)
                int deleteScore = dp[i - 1][j] + scoringMatrix.getGapPenalty(char1);
                // Score for inserting a character into seq1 (aligning seq2 char with a gap)
                int insertScore = dp[i][j - 1] + scoringMatrix.getGapPenalty(char2);

                dp[i][j] = Math.max(matchScore, Math.max(deleteScore, insertScore));
            }
        }

        // The final score is in the bottom-right cell
        return dp[len1][len2];
    }
}