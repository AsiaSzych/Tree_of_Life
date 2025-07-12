package com.phylogenetic.tree;

import java.util.ArrayList;
import java.util.List;

/**
 * Represents a node in the phylogenetic tree.
 * Can be either a leaf node (species) or an internal node (common ancestor).
 */
public class PhylogeneticNode {
  private final String name;
  private final double height;  // Similarity score at which this node was created
  private final List<PhylogeneticNode> children;
  private PhylogeneticNode parent;
  private final boolean isLeaf;
  
  // Constructor for leaf nodes (species)
  public PhylogeneticNode(String speciesName) {
    this.name = speciesName;
    this.height = 0.0;  // Leaf nodes are at height 0
    this.children = new ArrayList<>();
    this.isLeaf = true;
  }
  
  // Constructor for internal nodes
  public PhylogeneticNode(PhylogeneticNode left, PhylogeneticNode right, double height) {
    this.name = "(" + left.getName() + "," + right.getName() + ")";
    this.height = height;
    this.children = new ArrayList<>();
    this.children.add(left);
    this.children.add(right);
    left.setParent(this);
    right.setParent(this);
    this.isLeaf = false;
  }
  
  /**
   * Get all leaf nodes (species) under this node.
   */
  public List<String> getLeafNames() {
    List<String> leaves = new ArrayList<>();
    if (isLeaf) {
      leaves.add(name);
    } else {
      for (PhylogeneticNode child : children) {
        leaves.addAll(child.getLeafNames());
      }
    }
    return leaves;
  }
  
  /**
   * Calculate the distance from this node to the root.
   */
  public double getDistanceToRoot() {
    if (parent == null) {
      return 0;
    }
    return parent.height - this.height + parent.getDistanceToRoot();
  }
  
  // Getters and setters
  public String getName() {
    return name;
  }
  
  public double getHeight() {
    return height;
  }
  
  public List<PhylogeneticNode> getChildren() {
    return new ArrayList<>(children);
  }
  
  public PhylogeneticNode getParent() {
    return parent;
  }
  
  public void setParent(PhylogeneticNode parent) {
    this.parent = parent;
  }
  
  public boolean isLeaf() {
    return isLeaf;
  }
  
  public PhylogeneticNode getLeft() {
    return children.isEmpty() ? null : children.get(0);
  }
  
  public PhylogeneticNode getRight() {
    return children.size() < 2 ? null : children.get(1);
  }
}