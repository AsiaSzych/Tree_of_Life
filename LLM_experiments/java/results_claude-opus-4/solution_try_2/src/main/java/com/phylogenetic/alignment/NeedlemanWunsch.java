package com.phylogenetic.alignment;

import com.phylogenetic.model.BlosumMatrix;

/**
 * Implementation of the Needleman-Wunsch algorithm for global sequence alignment.
 */
public class NeedlemanWunsch {
  private final BlosumMatrix blosumMatrix;
  
  public NeedlemanWunsch(BlosumMatrix blosumMatrix) {
    this.blosumMatrix = blosumMatrix;
  }
  
  /**
   * Calculate the alignment score between two sequences.
   */
  public int align(String sequence1, String sequence2) {
    int m = sequence1.length();
    int n = sequence2.length();
    
    // Initialize the scoring matrix
    int[][] dp = new int[m + 1][n + 1];
    
    // Initialize first row (gaps in sequence1)
    dp[0][0] = 0;
    for (int j = 1; j <= n; j++) {
      dp[0][j] = dp[0][j - 1] + blosumMatrix.getGapPenalty(sequence2.charAt(j - 1));
    }
    
    // Initialize first column (gaps in sequence2)
    for (int i = 1; i <= m; i++) {
      dp[i][0] = dp[i - 1][0] + blosumMatrix.getGapPenalty(sequence1.charAt(i - 1));
    }
    
    // Fill the scoring matrix
    for (int i = 1; i <= m; i++) {
      for (int j = 1; j <= n; j++) {
        char char1 = sequence1.charAt(i - 1);
        char char2 = sequence2.charAt(j - 1);
        
        // Match/mismatch score
        int matchScore = dp[i - 1][j - 1] + 
            blosumMatrix.getSubstitutionScore(char1, char2);
        
        // Gap in sequence2
        int gapScore1 = dp[i - 1][j] + blosumMatrix.getGapPenalty(char1);
        
        // Gap in sequence1
        int gapScore2 = dp[i][j - 1] + blosumMatrix.getGapPenalty(char2);
        
        // Take maximum
        dp[i][j] = Math.max(matchScore, Math.max(gapScore1, gapScore2));
      }
    }
    
    return dp[m][n];
  }
}