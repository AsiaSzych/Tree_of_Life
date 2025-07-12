package com.phylogenetic.alignment;

import com.phylogenetic.model.AlignmentResult;
import com.phylogenetic.model.Organism;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Calculates pairwise alignments for all organism pairs.
 */
public class PairwiseAlignmentCalculator {
  private static final Logger logger = LoggerFactory.getLogger(
      PairwiseAlignmentCalculator.class);
  private final NeedlemanWunsch aligner;

  public PairwiseAlignmentCalculator(NeedlemanWunsch aligner) {
    this.aligner = aligner;
  }

  /**
   * Calculate alignment scores for all pairs of organisms.
   * Returns a map for fast access to scores.
   */
  public Map<String, Map<String, Integer>> calculateAllPairwiseScores(
      List<Organism> organisms) {
    logger.info("Calculating pairwise alignments for {} organisms", organisms.size());
    
    Map<String, Map<String, Integer>> scoreMatrix = new HashMap<>();
    List<AlignmentResult> results = new ArrayList<>();
    
    // Initialize the score matrix
    for (Organism org : organisms) {
      scoreMatrix.put(org.name(), new HashMap<>());
    }
    
    // Calculate scores for all pairs
    for (int i = 0; i < organisms.size(); i++) {
      Organism org1 = organisms.get(i);
      
      for (int j = i; j < organisms.size(); j++) {
        Organism org2 = organisms.get(j);
        
        int score = aligner.align(org1.sequence(), org2.sequence());
        
        // Store score in both directions for fast access
        scoreMatrix.get(org1.name()).put(org2.name(), score);
        if (i != j) {
          scoreMatrix.get(org2.name()).put(org1.name(), score);
        }
        
        results.add(new AlignmentResult(org1.name(), org2.name(), score));
        logger.debug("Alignment score between {} and {}: {}", 
            org1.name(), org2.name(), score);
      }
    }
    
    logger.info("Completed {} pairwise alignments", results.size());
    return scoreMatrix;
  }
}