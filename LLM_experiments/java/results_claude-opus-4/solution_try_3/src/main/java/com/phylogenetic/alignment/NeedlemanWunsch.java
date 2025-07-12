package com.phylogenetic.alignment;

import com.phylogenetic.model.BlosumMatrix;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Implementation of the Needleman-Wunsch algorithm for global sequence alignment.
 */
public class NeedlemanWunsch {
  private static final Logger logger = LoggerFactory.getLogger(NeedlemanWunsch.class);
  private final BlosumMatrix blosumMatrix;

  public NeedlemanWunsch(BlosumMatrix blosumMatrix) {
    this.blosumMatrix = blosumMatrix;
  }

  /**
   * Calculate the alignment score between two sequences.
   */
  public int align(String sequence1, String sequence2) {
    if (sequence1 == null || sequence2 == null) {
      throw new IllegalArgumentException("Sequences cannot be null");
    }

    int m = sequence1.length();
    int n = sequence2.length();
    
    // Initialize the scoring matrix
    int[][] scoreMatrix = new int[m + 1][n + 1];
    
    // Initialize first row and column with gap penalties
    for (int i = 1; i <= m; i++) {
      scoreMatrix[i][0] = scoreMatrix[i - 1][0] 
          + blosumMatrix.getGapPenalty(sequence1.charAt(i - 1));
    }
    
    for (int j = 1; j <= n; j++) {
      scoreMatrix[0][j] = scoreMatrix[0][j - 1] 
          + blosumMatrix.getGapPenalty(sequence2.charAt(j - 1));
    }
    
    // Fill the scoring matrix
    for (int i = 1; i <= m; i++) {
      for (int j = 1; j <= n; j++) {
        char char1 = sequence1.charAt(i - 1);
        char char2 = sequence2.charAt(j - 1);
        
        // Match/mismatch score
        int matchScore = scoreMatrix[i - 1][j - 1] 
            + blosumMatrix.getSubstitutionScore(char1, char2);
        
        // Gap in sequence2
        int gapScore1 = scoreMatrix[i - 1][j] 
            + blosumMatrix.getGapPenalty(char1);
        
        // Gap in sequence1
        int gapScore2 = scoreMatrix[i][j - 1] 
            + blosumMatrix.getGapPenalty(char2);
        
        // Take maximum score
        scoreMatrix[i][j] = Math.max(matchScore, Math.max(gapScore1, gapScore2));
      }
    }
    
    int finalScore = scoreMatrix[m][n];
    logger.debug("Alignment score for sequences of length {} and {}: {}", 
        m, n, finalScore);
    
    return finalScore;
  }
}