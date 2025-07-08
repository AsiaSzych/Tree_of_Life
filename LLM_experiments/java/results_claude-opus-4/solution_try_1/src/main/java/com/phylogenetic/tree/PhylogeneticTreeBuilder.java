package com.phylogenetic.tree;

import com.phylogenetic.model.AlignmentResult;
import com.phylogenetic.model.Organism;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Builds a phylogenetic tree using single-linkage hierarchical clustering
 * based on similarity scores.
 */
public class PhylogeneticTreeBuilder {
  private static final Logger logger = LoggerFactory.getLogger(PhylogeneticTreeBuilder.class);
  
  /**
   * Builds a phylogenetic tree from alignment results.
   *
   * @param organisms list of organisms
   * @param alignmentResults pairwise alignment scores
   * @return root node of the phylogenetic tree
   */
  public PhylogeneticNode buildTree(
      List<Organism> organisms, 
      Map<String, AlignmentResult> alignmentResults) {
    
    logger.info("Building phylogenetic tree for {} organisms", organisms.size());
    
    // Initialize clusters - each organism starts as its own cluster
    List<PhylogeneticNode> clusters = new ArrayList<>();
    Map<String, Integer> nameToIndex = new HashMap<>();
    
    for (int i = 0; i < organisms.size(); i++) {
      String name = organisms.get(i).name();
      clusters.add(new PhylogeneticNode(name));
      nameToIndex.put(name, i);
    }
    
    // Create similarity matrix for active clusters
    int n = organisms.size();
    Integer[][] similarityMatrix = new Integer[n][n];
    
    // Fill similarity matrix
    for (AlignmentResult result : alignmentResults.values()) {
      int i = nameToIndex.get(result.organism1());
      int j = nameToIndex.get(result.organism2());
      similarityMatrix[i][j] = result.score();
      similarityMatrix[j][i] = result.score();
    }
    
    // Build tree using agglomerative clustering
    while (clusters.size() > 1) {
      // Find the pair with highest similarity
      int maxScore = Integer.MIN_VALUE;
      int bestI = -1, bestJ = -1;
      
      for (int i = 0; i < clusters.size(); i++) {
        for (int j = i + 1; j < clusters.size(); j++) {
          Integer score = findMaxSimilarity(
              clusters.get(i), clusters.get(j), 
              similarityMatrix, nameToIndex);
          
          if (score != null && score > maxScore) {
            maxScore = score;
            bestI = i;
            bestJ = j;
          }
        }
      }
      
      if (bestI == -1) {
        throw new IllegalStateException("No valid pairs found for merging");
      }
      
      // Merge the two most similar clusters
      PhylogeneticNode merged = new PhylogeneticNode(
          clusters.get(bestI), 
          clusters.get(bestJ), 
          maxScore
      );
      
      logger.debug("Merging clusters at similarity score {}: {} and {}", 
          maxScore, 
          clusters.get(bestI).getName(), 
          clusters.get(bestJ).getName());
      
      // Remove old clusters and add merged one
      PhylogeneticNode cluster1 = clusters.get(bestI);
      PhylogeneticNode cluster2 = clusters.get(bestJ);
      clusters.remove(Math.max(bestI, bestJ));
      clusters.remove(Math.min(bestI, bestJ));
      clusters.add(merged);
    }
    
    logger.info("Tree construction complete");
    return clusters.get(0);
  }
  
  /**
   * Finds maximum similarity between any members of two clusters (single linkage).
   *
   * @param cluster1 first cluster
   * @param cluster2 second cluster
   * @param similarityMatrix matrix of pairwise similarities
   * @param nameToIndex mapping from species names to matrix indices
   * @return maximum similarity score between clusters
   */
  private Integer findMaxSimilarity(
      PhylogeneticNode cluster1, 
      PhylogeneticNode cluster2,
      Integer[][] similarityMatrix,
      Map<String, Integer> nameToIndex) {
    
    Integer maxSimilarity = null;
    
    for (String name1 : cluster1.getLeafNames()) {
      for (String name2 : cluster2.getLeafNames()) {
        Integer index1 = nameToIndex.get(name1);
        Integer index2 = nameToIndex.get(name2);
        
        if (index1 != null && index2 != null) {
          Integer score = similarityMatrix[index1][index2];
          if (score != null) {
            if (maxSimilarity == null || score > maxSimilarity) {
              maxSimilarity = score;
            }
          }
        }
      }
    }
    
    return maxSimilarity;
  }
}