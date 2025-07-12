package com.phylogenetic.io;

import com.phylogenetic.tree.NewickFormatter;
import com.phylogenetic.tree.PhylogeneticTree;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Writes phylogenetic trees to Newick format files.
 */
public class NewickWriter {
  private static final Logger logger = LoggerFactory.getLogger(NewickWriter.class);
  private final NewickFormatter formatter;
  
  public NewickWriter() {
    this.formatter = new NewickFormatter();
  }
  
  /**
   * Save tree in both Newick formats.
   * 
   * @param tree The phylogenetic tree to save
   * @param blosumType The BLOSUM matrix type used (e.g., "50" or "62")
   * @throws IOException if file writing fails
   */
  public void saveTree(PhylogeneticTree tree, String blosumType) throws IOException {
    // Save simple format
    String simpleFilename = String.format("tree_blosum%s_newick.nw", blosumType);
    saveNewickSimple(tree, simpleFilename);
    
    // Save format with distances
    String distanceFilename = String.format("tree_blosum%s_newick_with_distance.nw", 
        blosumType);
    saveNewickWithDistances(tree, distanceFilename);
  }
  
  /**
   * Save tree in simple Newick format (no distances).
   */
  private void saveNewickSimple(PhylogeneticTree tree, String filename) 
      throws IOException {
    logger.info("Saving tree to {} (simple format)", filename);
    
    String newick = formatter.toNewickSimple(tree.getRoot());
    
    try (BufferedWriter writer = new BufferedWriter(new FileWriter(filename))) {
      writer.write(newick);
      writer.newLine();
    }
    
    logger.info("Successfully saved simple Newick format");
  }
  
  /**
   * Save tree in Newick format with branch distances.
   */
  private void saveNewickWithDistances(PhylogeneticTree tree, String filename) 
      throws IOException {
    logger.info("Saving tree to {} (with distances)", filename);
    
    String newick = formatter.toNewickWithDistances(tree.getRoot());
    
    try (BufferedWriter writer = new BufferedWriter(new FileWriter(filename))) {
      writer.write(newick);
      writer.newLine();
    }
    
    logger.info("Successfully saved Newick format with distances");
  }
}