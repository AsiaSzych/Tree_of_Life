package com.phylogenetic.alignment;

import com.phylogenetic.io.ResultWriter;
import com.phylogenetic.model.AlignmentResult;
import com.phylogenetic.model.BlosumMatrix;
import com.phylogenetic.model.Organism;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.logging.Logger;

/**
 * Service for managing pairwise sequence alignments.
 */
public class AlignmentService {
  private static final Logger LOGGER = Logger.getLogger(AlignmentService.class.getName());
  
  private final NeedlemanWunsch aligner;
  private final Map<String, Integer> scoreMatrix;
  private final BlosumMatrix blosumMatrix;
  private final ResultWriter resultWriter;
  
  public AlignmentService(BlosumMatrix blosumMatrix) {
    this.aligner = new NeedlemanWunsch(blosumMatrix);
    this.scoreMatrix = new HashMap<>();
    this.blosumMatrix = blosumMatrix;
    this.resultWriter = new ResultWriter();
  }
  
  /**
   * Calculate alignment scores for all pairs of organisms and save to file.
   */
  public List<AlignmentResult> calculateAllPairwiseScores(List<Organism> organisms) 
      throws IOException {
    List<AlignmentResult> results = new ArrayList<>();
    
    for (int i = 0; i < organisms.size(); i++) {
      for (int j = i + 1; j < organisms.size(); j++) {
        Organism org1 = organisms.get(i);
        Organism org2 = organisms.get(j);
        
        int score = aligner.align(org1.sequence(), org2.sequence());
        
        // Store in both directions for fast access
        String key1 = createKey(org1.name(), org2.name());
        String key2 = createKey(org2.name(), org1.name());
        scoreMatrix.put(key1, score);
        scoreMatrix.put(key2, score);
        
        results.add(new AlignmentResult(org1.name(), org2.name(), score));
      }
    }
    
    // Save results to file
    resultWriter.saveAlignmentScores(results, blosumMatrix.getType());
    LOGGER.info("Saved alignment scores to organisms_scores_blosum" + 
                blosumMatrix.getType() + ".json");
    
    return results;
  }
  
  /**
   * Get the alignment score between two organisms.
   */
  public int getScore(String organism1, String organism2) {
    String key = createKey(organism1, organism2);
    Integer score = scoreMatrix.get(key);
    if (score == null) {
      throw new IllegalArgumentException(
          "No alignment score found for: " + organism1 + " and " + organism2);
    }
    return score;
  }
  
  /**
   * Get all calculated scores as a map.
   */
  public Map<String, Integer> getAllScores() {
    return new HashMap<>(scoreMatrix);
  }
  
  private String createKey(String org1, String org2) {
    return org1 + "|" + org2;
  }
}