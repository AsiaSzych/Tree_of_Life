package com.phylogenetic.alignment;

import com.phylogenetic.model.AlignmentResult;
import com.phylogenetic.model.BlosumMatrix;
import com.phylogenetic.model.Organism;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Manages pairwise sequence alignments for multiple organisms.
 */
public class SequenceAligner {
  private static final Logger logger = LoggerFactory.getLogger(SequenceAligner.class);
  private final NeedlemanWunsch aligner;
  
  public SequenceAligner(BlosumMatrix blosumMatrix) {
    this.aligner = new NeedlemanWunsch(blosumMatrix);
  }
  
  /**
   * Calculates alignment scores for all pairs of organisms.
   *
   * @param organisms list of organisms to align
   * @return map of alignment results keyed by organism pair
   */
  public Map<String, AlignmentResult> alignAllPairs(List<Organism> organisms) {
    Map<String, AlignmentResult> results = new HashMap<>();
    int totalPairs = organisms.size() * (organisms.size() - 1) / 2;
    logger.info("Starting alignment of {} organism pairs", totalPairs);
    
    int completed = 0;
    for (int i = 0; i < organisms.size(); i++) {
      for (int j = i + 1; j < organisms.size(); j++) {
        Organism org1 = organisms.get(i);
        Organism org2 = organisms.get(j);
        
        int score = aligner.calculateScore(org1.sequence(), org2.sequence());
        AlignmentResult result = new AlignmentResult(org1.name(), org2.name(), score);
        
        results.put(result.getPairKey(), result);
        completed++;
        
        if (completed % 10 == 0 || completed == totalPairs) {
          logger.debug("Completed {}/{} alignments", completed, totalPairs);
        }
      }
    }
    
    logger.info("Alignment complete. Calculated {} scores", results.size());
    return results;
  }
  
  /**
   * Creates a distance matrix from alignment results.
   * Higher alignment scores indicate greater similarity.
   *
   * @param organisms list of organisms
   * @param alignmentResults map of alignment results
   * @return 2D array representing distance matrix
   */
  public int[][] createDistanceMatrix(
      List<Organism> organisms, 
      Map<String, AlignmentResult> alignmentResults) {
    
    int n = organisms.size();
    int[][] matrix = new int[n][n];
    
    for (int i = 0; i < n; i++) {
      for (int j = 0; j < n; j++) {
        if (i == j) {
          matrix[i][j] = 0;
        } else {
          String org1 = organisms.get(i).name();
          String org2 = organisms.get(j).name();
          String key = org1.compareTo(org2) < 0 
              ? org1 + "|" + org2 
              : org2 + "|" + org1;
          
          AlignmentResult result = alignmentResults.get(key);
          if (result != null) {
            // Store the alignment score directly
            matrix[i][j] = result.score();
          }
        }
      }
    }
    
    return matrix;
  }
}