package com.phylogenetic.alignment;

import com.phylogenetic.model.BlosumMatrix;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Implementation of the Needleman-Wunsch global sequence alignment algorithm.
 */
public class NeedlemanWunsch {
  private static final Logger logger = LoggerFactory.getLogger(NeedlemanWunsch.class);
  private final BlosumMatrix blosumMatrix;
  
  public NeedlemanWunsch(BlosumMatrix blosumMatrix) {
    this.blosumMatrix = blosumMatrix;
  }
  
  /**
   * Calculates the alignment score between two sequences.
   *
   * @param sequence1 first amino acid sequence
   * @param sequence2 second amino acid sequence
   * @return the alignment score
   */
  public int calculateScore(String sequence1, String sequence2) {
    int m = sequence1.length();
    int n = sequence2.length();
    
    // Initialize the scoring matrix
    int[][] scoreMatrix = new int[m + 1][n + 1];
    
    // Initialize first row with gap penalties
    for (int j = 1; j <= n; j++) {
      scoreMatrix[0][j] = scoreMatrix[0][j - 1] 
          + blosumMatrix.getGapPenalty(sequence2.charAt(j - 1));
    }
    
    // Initialize first column with gap penalties
    for (int i = 1; i <= m; i++) {
      scoreMatrix[i][0] = scoreMatrix[i - 1][0] 
          + blosumMatrix.getGapPenalty(sequence1.charAt(i - 1));
    }
    
    // Fill the scoring matrix
    for (int i = 1; i <= m; i++) {
      for (int j = 1; j <= n; j++) {
        char char1 = sequence1.charAt(i - 1);
        char char2 = sequence2.charAt(j - 1);
        
        // Calculate scores for three possible operations
        int matchScore = scoreMatrix[i - 1][j - 1] 
            + blosumMatrix.getSubstitutionScore(char1, char2);
        int deleteScore = scoreMatrix[i - 1][j] 
            + blosumMatrix.getGapPenalty(char1);
        int insertScore = scoreMatrix[i][j - 1] 
            + blosumMatrix.getGapPenalty(char2);
        
        // Take the maximum score
        scoreMatrix[i][j] = Math.max(matchScore, Math.max(deleteScore, insertScore));
      }
    }
    
    return scoreMatrix[m][n];
  }
}