package com.phylogenetic.tree;

import java.util.ArrayList;
import java.util.List;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Provides analysis functions for phylogenetic trees.
 */
public class TreeAnalyzer {
  private static final Logger logger = LoggerFactory.getLogger(TreeAnalyzer.class);
  
  /**
   * Extracts clusters from the tree at a given similarity threshold.
   *
   * @param root root of the phylogenetic tree
   * @param threshold minimum similarity score for clustering
   * @return list of clusters (each cluster is a list of species names)
   */
  public List<List<String>> getClustersAtThreshold(PhylogeneticNode root, double threshold) {
    logger.info("Extracting clusters at threshold: {}", threshold);
    
    List<List<String>> clusters = new ArrayList<>();
    root.getClustersAtThreshold(threshold, clusters);
    
    logger.info("Found {} clusters at threshold {}", clusters.size(), threshold);
    return clusters;
  }
  
  /**
   * Gets the height (similarity score) of the root node.
   *
   * @param root root of the phylogenetic tree
   * @return height of the tree
   */
  public double getTreeHeight(PhylogeneticNode root) {
    return root.getHeight();
  }
  
  /**
   * Counts the total number of leaves (species) in the tree.
   *
   * @param root root of the phylogenetic tree
   * @return number of species
   */
  public int countSpecies(PhylogeneticNode root) {
    return root.getLeafNames().size();
  }
  
  /**
   * Generates a summary of the tree structure.
   *
   * @param root root of the phylogenetic tree
   * @return tree summary
   */
  public String getTreeSummary(PhylogeneticNode root) {
    StringBuilder summary = new StringBuilder();
    summary.append("Phylogenetic Tree Summary:\n");
    summary.append("- Total species: ").append(countSpecies(root)).append("\n");
    summary.append("- Tree height: ").append(getTreeHeight(root)).append("\n");
    summary.append("- Root node: ").append(root.getName()).append("\n");
    return summary.toString();
  }
}