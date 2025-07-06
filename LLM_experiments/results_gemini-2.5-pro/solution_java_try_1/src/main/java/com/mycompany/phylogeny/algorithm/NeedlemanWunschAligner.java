package com.mycompany.phylogeny.algorithm;

import com.mycompany.phylogeny.domain.ScoringMatrix;
import java.util.Objects;

/**
 * Implements the Needleman-Wunsch algorithm for global sequence alignment.
 */
public class NeedlemanWunschAligner {

  private final ScoringMatrix scoringMatrix;

  public NeedlemanWunschAligner(ScoringMatrix scoringMatrix) {
    this.scoringMatrix = Objects.requireNonNull(scoringMatrix, "ScoringMatrix cannot be null.");
  }

  /**
   * Calculates the optimal alignment score between two sequences.
   *
   * @param seq1 The first sequence.
   * @param seq2 The second sequence.
   * @return The alignment score as an integer.
   */
  public int calculateScore(String seq1, String seq2) {
    int m = seq1.length();
    int n = seq2.length();

    int[][] dp = new int[m + 1][n + 1];

    // Initialize the DP table for gaps
    for (int i = 1; i <= m; i++) {
      dp[i][0] = dp[i - 1][0] + scoringMatrix.getGapPenalty(seq1.charAt(i - 1));
    }
    for (int j = 1; j <= n; j++) {
      dp[0][j] = dp[0][j - 1] + scoringMatrix.getGapPenalty(seq2.charAt(j - 1));
    }

    // Fill the DP table
    for (int i = 1; i <= m; i++) {
      for (int j = 1; j <= n; j++) {
        char char1 = seq1.charAt(i - 1);
        char char2 = seq2.charAt(j - 1);

        int matchScore = dp[i - 1][j - 1] + scoringMatrix.getSubstitutionScore(char1, char2);
        int deleteScore = dp[i - 1][j] + scoringMatrix.getGapPenalty(char1); // Gap in seq2
        int insertScore = dp[i][j - 1] + scoringMatrix.getGapPenalty(char2); // Gap in seq1

        dp[i][j] = Math.max(matchScore, Math.max(deleteScore, insertScore));
      }
    }

    return dp[m][n];
  }
}