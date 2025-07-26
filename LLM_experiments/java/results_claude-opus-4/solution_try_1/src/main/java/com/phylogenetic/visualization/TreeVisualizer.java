package com.phylogenetic.visualization;

import com.phylogenetic.tree.PhylogeneticNode;
import java.io.IOException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Main interface for tree visualization operations.
 */
public class TreeVisualizer {
  private static final Logger logger = LoggerFactory.getLogger(TreeVisualizer.class);
  private final DendrogramDrawer dendrogramDrawer;
  
  public TreeVisualizer() {
    this.dendrogramDrawer = new DendrogramDrawer();
  }
  
  /**
   * Creates all visualizations for the phylogenetic tree.
   *
   * @param root root of the phylogenetic tree
   * @param blosumType BLOSUM matrix type used
   * @throws IOException if files cannot be saved
   */
  public void visualizeTree(PhylogeneticNode root, String blosumType) throws IOException {
    logger.info("Creating tree visualizations for {}", blosumType);
    
    // Create dendrogram
    dendrogramDrawer.drawDendrogram(root, blosumType);
    
    logger.info("All visualizations completed");
  }
}
