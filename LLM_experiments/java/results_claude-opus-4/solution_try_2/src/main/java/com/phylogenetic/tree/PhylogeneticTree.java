package com.phylogenetic.tree;

import java.util.ArrayList;
import java.util.List;

/**
 * Represents a complete phylogenetic tree.
 */
public class PhylogeneticTree {
  private final PhylogeneticNode root;
  
  public PhylogeneticTree(PhylogeneticNode root) {
    this.root = root;
  }
  
  /**
   * Get clusters at a specific similarity threshold.
   * Cuts the tree at the given threshold and returns groups of species.
   */
  public List<List<String>> getClustersAtThreshold(double threshold) {
    List<List<String>> clusters = new ArrayList<>();
    getClustersRecursive(root, threshold, clusters);
    return clusters;
  }
  
  private void getClustersRecursive(PhylogeneticNode node, double threshold, 
                                    List<List<String>> clusters) {
    if (node.getHeight() <= threshold || node.isLeaf()) {
      // This node and all its descendants form a cluster
      clusters.add(node.getLeafNames());
    } else {
      // Continue searching in children
      for (PhylogeneticNode child : node.getChildren()) {
        getClustersRecursive(child, threshold, clusters);
      }
    }
  }
  
  /**
   * Convert the tree to Newick format without distances.
   * Example output: "(A,B,(C,D));"
   */
  public String toNewickSimple() {
    return toNewickSimpleRecursive(root) + ";";
  }
  
  private String toNewickSimpleRecursive(PhylogeneticNode node) {
    if (node.isLeaf()) {
      return node.getName();
    } else {
      StringBuilder sb = new StringBuilder("(");
      List<PhylogeneticNode> children = node.getChildren();
      for (int i = 0; i < children.size(); i++) {
        if (i > 0) sb.append(",");
        sb.append(toNewickSimpleRecursive(children.get(i)));
      }
      sb.append(")");
      return sb.toString();
    }
  }
  
  /**
   * Convert the tree to Newick format with integer distances.
   * Example output: "(A:1,B:2,(C:3,D:4):5);"
   */
  public String toNewickWithDistances() {
    return toNewickWithDistancesRecursive(root) + ";";
  }
  
  private String toNewickWithDistancesRecursive(PhylogeneticNode node) {
    if (node.isLeaf()) {
      return node.getName();
    } else {
      StringBuilder sb = new StringBuilder("(");
      List<PhylogeneticNode> children = node.getChildren();
      for (int i = 0; i < children.size(); i++) {
        if (i > 0) sb.append(",");
        PhylogeneticNode child = children.get(i);
        sb.append(toNewickWithDistancesRecursive(child));
        // Add branch length as integer (difference in heights)
        int branchLength = (int) Math.round(node.getHeight() - child.getHeight());
        sb.append(":").append(branchLength);
      }
      sb.append(")");
      return sb.toString();
    }
  }
  
  public PhylogeneticNode getRoot() {
    return root;
  }
  
  /**
   * Get all species names in the tree.
   */
  public List<String> getAllSpecies() {
    return root.getLeafNames();
  }
  
  /**
   * Get the height of the tree (root height).
   */
  public double getHeight() {
    return root.getHeight();
  }
}