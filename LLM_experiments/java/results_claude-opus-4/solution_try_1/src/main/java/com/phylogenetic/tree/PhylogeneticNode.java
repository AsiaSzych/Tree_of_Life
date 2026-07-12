package com.phylogenetic.tree;

import java.util.ArrayList;
import java.util.List;

/**
 * Represents a node in the phylogenetic tree.
 * Can be either a leaf node (species) or an internal node (ancestor).
 */
public class PhylogeneticNode {
  private final String name;
  private final boolean isLeaf;
  private final double height; // Similarity score at which this node was created
  private PhylogeneticNode left;
  private PhylogeneticNode right;
  private final List<String> leafNames; // All species under this node
  
  /**
   * Creates a leaf node representing a species.
   *
   * @param speciesName name of the species
   */
  public PhylogeneticNode(String speciesName) {
    this.name = speciesName;
    this.isLeaf = true;
    this.height = 0.0; // Leaf nodes are at height 0
    this.leafNames = new ArrayList<>();
    this.leafNames.add(speciesName);
  }
  
  /**
   * Creates an internal node by merging two existing nodes.
   *
   * @param left left child node
   * @param right right child node
   * @param height similarity score at merge point
   */
  public PhylogeneticNode(PhylogeneticNode left, PhylogeneticNode right, double height) {
    this.left = left;
    this.right = right;
    this.height = height;
    this.isLeaf = false;
    this.name = "(" + left.getName() + "," + right.getName() + ")";
    
    // Combine leaf names from both children
    this.leafNames = new ArrayList<>();
    this.leafNames.addAll(left.getLeafNames());
    this.leafNames.addAll(right.getLeafNames());
  }
  
  /**
   * Gets all clusters at or above the specified similarity threshold.
   * Modified to handle the case where we "forget" nodes below threshold.
   *
   * @param threshold minimum similarity score for clustering
   * @param clusters list to accumulate clusters
   */
  public void getClustersAtThreshold(double threshold, List<List<String>> clusters) {
    if (isLeaf) {
      // A single leaf forms its own cluster if not part of a larger one
      List<String> singleCluster = new ArrayList<>();
      singleCluster.add(name);
      clusters.add(singleCluster);
    } else if (height >= threshold) {
      // This entire subtree forms a cluster
      clusters.add(new ArrayList<>(leafNames));
    } else {
      // Height is below threshold, process children separately
      if (left != null) {
        left.getClustersAtThreshold(threshold, clusters);
      }
      if (right != null) {
        right.getClustersAtThreshold(threshold, clusters);
      }
    }
  }
  
  /**
   * Converts the tree to Newick format without distances.
   *
   * @return Newick representation without branch lengths
   */
  public String toNewickSimple() {
    if (isLeaf) {
      return name;
    } else {
      return String.format("(%s,%s)", 
          left.toNewickSimple(), 
          right.toNewickSimple());
    }
  }
  
  /**
   * Converts the tree to Newick format with distances.
   * Distances are formatted as integers.
   *
   * @return Newick representation with branch lengths
   */
  public String toNewickWithDistances() {
    if (isLeaf) {
      return name;
    } else {
      // Calculate branch lengths as integers
      int leftDistance = (int)(height - left.height);
      int rightDistance = (int)(height - right.height);
      
      String leftSubtree = left.toNewickWithDistances();
      String rightSubtree = right.toNewickWithDistances();
      
      // Add distances to non-leaf children
      if (!left.isLeaf) {
        leftSubtree = leftSubtree + ":" + leftDistance;
      } else {
        leftSubtree = leftSubtree + ":" + leftDistance;
      }
      
      if (!right.isLeaf) {
        rightSubtree = rightSubtree + ":" + rightDistance;
      } else {
        rightSubtree = rightSubtree + ":" + rightDistance;
      }
      
      return String.format("(%s,%s)", leftSubtree, rightSubtree);
    }
  }
  
  // Getters
  public String getName() {
    return name;
  }
  
  public boolean isLeaf() {
    return isLeaf;
  }
  
  public double getHeight() {
    return height;
  }
  
  public PhylogeneticNode getLeft() {
    return left;
  }
  
  public PhylogeneticNode getRight() {
    return right;
  }
  
  public List<String> getLeafNames() {
    return new ArrayList<>(leafNames);
  }
}