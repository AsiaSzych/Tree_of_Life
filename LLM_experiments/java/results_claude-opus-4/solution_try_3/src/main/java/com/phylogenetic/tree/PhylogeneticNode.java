package com.phylogenetic.tree;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/**
 * Represents a node in the phylogenetic tree.
 * Can be either a leaf node (species) or an internal node (common ancestor).
 */
public class PhylogeneticNode {
  private final String name;
  private final PhylogeneticNode left;
  private final PhylogeneticNode right;
  private final int height; // Similarity score at which this node was created
  private final boolean isLeaf;
  
  // Constructor for leaf nodes (species)
  public PhylogeneticNode(String name) {
    this.name = Objects.requireNonNull(name, "Node name cannot be null");
    this.left = null;
    this.right = null;
    this.height = 0;
    this.isLeaf = true;
  }
  
  // Constructor for internal nodes (merge points)
  public PhylogeneticNode(String name, PhylogeneticNode left, 
      PhylogeneticNode right, int height) {
    this.name = Objects.requireNonNull(name, "Node name cannot be null");
    this.left = Objects.requireNonNull(left, "Left child cannot be null");
    this.right = Objects.requireNonNull(right, "Right child cannot be null");
    this.height = height;
    this.isLeaf = false;
  }
  
  /**
   * Get all leaf nodes (species) under this node.
   */
  public List<String> getLeafNames() {
    List<String> leaves = new ArrayList<>();
    collectLeaves(this, leaves);
    return leaves;
  }
  
  private void collectLeaves(PhylogeneticNode node, List<String> leaves) {
    if (node.isLeaf) {
      leaves.add(node.name);
    } else {
      if (node.left != null) {
        collectLeaves(node.left, leaves);
      }
      if (node.right != null) {
        collectLeaves(node.right, leaves);
      }
    }
  }
  
  /**
   * Get clusters at a given similarity threshold.
   * Nodes with height >= threshold are kept together.
   */
  public List<List<String>> getClustersAtThreshold(int threshold) {
    List<List<String>> clusters = new ArrayList<>();
    collectClusters(this, threshold, clusters);
    return clusters;
  }
  
  private void collectClusters(PhylogeneticNode node, int threshold, 
      List<List<String>> clusters) {
    if (node.isLeaf || node.height >= threshold) {
      // This node and all its descendants form a cluster
      clusters.add(node.getLeafNames());
    } else {
      // Split into subclusters
      if (node.left != null) {
        collectClusters(node.left, threshold, clusters);
      }
      if (node.right != null) {
        collectClusters(node.right, threshold, clusters);
      }
    }
  }
  
  // Getters
  public String getName() { return name; }
  public PhylogeneticNode getLeft() { return left; }
  public PhylogeneticNode getRight() { return right; }
  public int getHeight() { return height; }
  public boolean isLeaf() { return isLeaf; }
}