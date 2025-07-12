package com.phylogenetic.tree;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Formats phylogenetic trees in Newick format.
 */
public class NewickFormatter {
  private static final Logger logger = LoggerFactory.getLogger(NewickFormatter.class);
  
  /**
   * Convert tree to Newick format without distances.
   * Example: (A,B,(C,D));
   */
  public String toNewickSimple(PhylogeneticNode node) {
    if (node == null) {
      return "";
    }
    
    StringBuilder sb = new StringBuilder();
    buildNewickSimple(node, sb);
    sb.append(";");
    
    String result = sb.toString();
    logger.debug("Generated simple Newick: {}", result);
    return result;
  }
  
  /**
   * Convert tree to Newick format with branch distances.
   * Example: (A:1,B:2,(C:3,D:4):5);
   */
  public String toNewickWithDistances(PhylogeneticNode node) {
    if (node == null) {
      return "";
    }
    
    StringBuilder sb = new StringBuilder();
    buildNewickWithDistances(node, sb, 0);
    sb.append(";");
    
    String result = sb.toString();
    logger.debug("Generated Newick with distances: {}", result);
    return result;
  }
  
  /**
   * Recursively build simple Newick format.
   */
  private void buildNewickSimple(PhylogeneticNode node, StringBuilder sb) {
    if (node.isLeaf()) {
      sb.append(node.getName());
    } else {
      sb.append("(");
      buildNewickSimple(node.getLeft(), sb);
      sb.append(",");
      buildNewickSimple(node.getRight(), sb);
      sb.append(")");
    }
  }
  
  /**
   * Recursively build Newick format with distances.
   * Distance is calculated as the difference between parent and child heights.
   */
  private void buildNewickWithDistances(PhylogeneticNode node, StringBuilder sb, 
      int parentHeight) {
    if (node.isLeaf()) {
      sb.append(node.getName());
      // Leaf nodes have distance from their parent
      if (parentHeight > 0) {
        sb.append(":").append(parentHeight);
      }
    } else {
      sb.append("(");
      
      // Calculate branch length as difference in heights
      int leftDistance = node.getHeight() - getMaxHeight(node.getLeft());
      int rightDistance = node.getHeight() - getMaxHeight(node.getRight());
      
      buildNewickWithDistances(node.getLeft(), sb, leftDistance);
      sb.append(",");
      buildNewickWithDistances(node.getRight(), sb, rightDistance);
      sb.append(")");
      
      // Add distance from this node to its parent
      if (parentHeight > 0) {
        sb.append(":").append(parentHeight);
      }
    }
  }
  
  /**
   * Get the maximum height in a subtree (height of the root of subtree).
   */
  private int getMaxHeight(PhylogeneticNode node) {
    if (node == null) {
      return 0;
    }
    if (node.isLeaf()) {
      return 0;
    }
    return node.getHeight();
  }
}