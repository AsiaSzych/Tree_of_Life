package com.phylogenetic.tree;

import java.util.List;

/**
 * Represents a complete phylogenetic tree with its root node.
 */
public class PhylogeneticTree {
  private final PhylogeneticNode root;
  private final int minScore;
  private final int maxScore;
  
  public PhylogeneticTree(PhylogeneticNode root, int minScore, int maxScore) {
    this.root = root;
    this.minScore = minScore;
    this.maxScore = maxScore;
  }
  
  public PhylogeneticNode getRoot() {
    return root;
  }
  
  public int getMinScore() {
    return minScore;
  }
  
  public int getMaxScore() {
    return maxScore;
  }
  
  /**
   * Get all species names in the tree.
   */
  public List<String> getAllSpecies() {
    return root.getLeafNames();
  }
  
  /**
   * Get clusters at a specific similarity threshold.
   */
  public List<List<String>> getClustersAtThreshold(int threshold) {
    if (threshold < minScore || threshold > maxScore) {
      throw new IllegalArgumentException(
          String.format("Threshold %d is outside the valid range [%d, %d]", 
              threshold, minScore, maxScore));
    }
    return root.getClustersAtThreshold(threshold);
  }
}