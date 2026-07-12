package com.phylogenetic.tree;

/**
 * Represents a pair of clusters with their similarity score.
 * Used during tree construction to track which clusters to merge next.
 */
public class ClusterPair implements Comparable<ClusterPair> {
  private final int cluster1Index;
  private final int cluster2Index;
  private final int similarityScore;
  
  public ClusterPair(int cluster1Index, int cluster2Index, int similarityScore) {
    this.cluster1Index = cluster1Index;
    this.cluster2Index = cluster2Index;
    this.similarityScore = similarityScore;
  }
  
  @Override
  public int compareTo(ClusterPair other) {
    // Higher similarity scores should come first (descending order)
    return Integer.compare(other.similarityScore, this.similarityScore);
  }
  
  public int getCluster1Index() {
    return cluster1Index;
  }
  
  public int getCluster2Index() {
    return cluster2Index;
  }
  
  public int getSimilarityScore() {
    return similarityScore;
  }
}