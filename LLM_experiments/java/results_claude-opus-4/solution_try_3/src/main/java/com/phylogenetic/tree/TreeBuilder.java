package com.phylogenetic.tree;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Builds a phylogenetic tree using single-linkage clustering.
 */
public class TreeBuilder {
  private static final Logger logger = LoggerFactory.getLogger(TreeBuilder.class);
  
  /**
   * Build a phylogenetic tree from similarity scores.
   */
  public PhylogeneticTree buildTree(Map<String, Map<String, Integer>> scoreMatrix) {
    logger.info("Building phylogenetic tree from {} species", scoreMatrix.size());
    
    // Initialize clusters - each species starts as its own cluster
    Map<String, PhylogeneticNode> clusters = new HashMap<>();
    for (String species : scoreMatrix.keySet()) {
      clusters.put(species, new PhylogeneticNode(species));
    }
    
    // Track min and max scores for validation
    int minScore = Integer.MAX_VALUE;
    int maxScore = Integer.MIN_VALUE;
    
    // Build similarity pairs for efficient processing
    List<SimilarityPair> pairs = buildSimilarityPairs(scoreMatrix);
    for (SimilarityPair pair : pairs) {
      minScore = Math.min(minScore, pair.score);
      maxScore = Math.max(maxScore, pair.score);
    }
    
    // Sort pairs by score (descending - highest similarity first)
    pairs.sort((a, b) -> Integer.compare(b.score, a.score));
    
    // Perform hierarchical clustering
    int mergeCount = 0;
    for (SimilarityPair pair : pairs) {
      if (clusters.size() == 1) {
        break; // Tree is complete
      }
      
      // Check if both clusters still exist (haven't been merged)
      if (clusters.containsKey(pair.species1) && clusters.containsKey(pair.species2)) {
        // Create new internal node
        PhylogeneticNode left = clusters.get(pair.species1);
        PhylogeneticNode right = clusters.get(pair.species2);
        
        String newNodeName = String.format("Node_%d", ++mergeCount);
        PhylogeneticNode newNode = new PhylogeneticNode(
            newNodeName, left, right, pair.score);
        
        logger.debug("Merging {} and {} at similarity score {}", 
            pair.species1, pair.species2, pair.score);
        
        // Remove old clusters
        clusters.remove(pair.species1);
        clusters.remove(pair.species2);
        
        // Add new cluster with combined name for further merging
        String combinedKey = pair.species1 + "_" + pair.species2;
        clusters.put(combinedKey, newNode);
        
        // Update score matrix for the new cluster
        updateScoreMatrix(scoreMatrix, pair.species1, pair.species2, 
            combinedKey, newNode);
      }
    }
    
    // The last remaining cluster is the root
    // if (clusters.size() != 1) {
    //   throw new IllegalStateException(
    //       "Tree construction failed. Remaining clusters: " + clusters.size());
    // }
    
    PhylogeneticNode root = clusters.values().iterator().next();
    logger.info("Tree construction complete. Root height: {}", root.getHeight());
    
    return new PhylogeneticTree(root, minScore, maxScore);
  }
  
  /**
   * Build list of all similarity pairs from the score matrix.
   */
  private List<SimilarityPair> buildSimilarityPairs(
      Map<String, Map<String, Integer>> scoreMatrix) {
    List<SimilarityPair> pairs = new ArrayList<>();
    Set<String> processed = new HashSet<>();
    
    for (Map.Entry<String, Map<String, Integer>> entry : scoreMatrix.entrySet()) {
      String species1 = entry.getKey();
      processed.add(species1);
      
      for (Map.Entry<String, Integer> innerEntry : entry.getValue().entrySet()) {
        String species2 = innerEntry.getKey();
        
        // Skip self-comparisons and already processed pairs
        if (!species1.equals(species2) && !processed.contains(species2)) {
          pairs.add(new SimilarityPair(species1, species2, innerEntry.getValue()));
        }
      }
    }
    
    return pairs;
  }
  
  /**
   * Update score matrix after merging two clusters.
   * Uses single-linkage: take maximum similarity to any member.
   */
  private void updateScoreMatrix(Map<String, Map<String, Integer>> scoreMatrix,
      String cluster1, String cluster2, String newClusterKey, 
      PhylogeneticNode newNode) {
    
    Map<String, Integer> newScores = new HashMap<>();
    
    // Get all species in the new cluster
    Set<String> mergedSpecies = new HashSet<>(
        newNode.getLeafNames());
    
    // Calculate scores between new cluster and all other entities
    for (String entity : scoreMatrix.keySet()) {
      if (!entity.equals(cluster1) && !entity.equals(cluster2)) {
        int maxScore = Integer.MIN_VALUE;
        
        // Find maximum score between any species in the clusters
        for (String speciesInNew : mergedSpecies) {
          if (scoreMatrix.containsKey(speciesInNew)) {
            Integer score = scoreMatrix.get(speciesInNew).get(entity);
            if (score == null && scoreMatrix.containsKey(entity)) {
              score = scoreMatrix.get(entity).get(speciesInNew);
            }
            if (score != null) {
              maxScore = Math.max(maxScore, score);
            }
          }
        }
        
        if (maxScore > Integer.MIN_VALUE) {
          newScores.put(entity, maxScore);
          // Update reverse direction
          scoreMatrix.get(entity).put(newClusterKey, maxScore);
        }
      }
    }
    
    scoreMatrix.put(newClusterKey, newScores);
  }
  
  /**
   * Helper class to store similarity pairs.
   */
  private static class SimilarityPair {
    final String species1;
    final String species2;
    final int score;
    
    SimilarityPair(String species1, String species2, int score) {
      this.species1 = species1;
      this.species2 = species2;
      this.score = score;
    }
  }
}