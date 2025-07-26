package com.phylogenetic.io;

import com.phylogenetic.tree.PhylogeneticNode;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Handles writing phylogenetic trees to Newick format files.
 */
public class NewickWriter {
  private static final Logger logger = LoggerFactory.getLogger(NewickWriter.class);
  
  /**
   * Saves the tree in both Newick format variations.
   *
   * @param root root of the phylogenetic tree
   * @param blosumType the BLOSUM matrix type used (e.g., "BLOSUM50", "BLOSUM62")
   * @throws IOException if files cannot be written
   */
  public void saveTree(PhylogeneticNode root, String blosumType) throws IOException {
    // Extract the number from BLOSUM type
    String blosumNumber = blosumType.replaceAll("[^0-9]", "");
    
    // Save simple Newick format (without distances)
    String simpleFilename = String.format("tree_blosum%s_newick.nw", blosumNumber);
    saveSimpleNewick(root, simpleFilename);
    
    // Save Newick format with distances
    String distanceFilename = String.format("tree_blosum%s_newick_with_distance.nw", 
        blosumNumber);
    saveNewickWithDistances(root, distanceFilename);
  }
  
  /**
   * Saves the tree in simple Newick format (leaf names only).
   *
   * @param root root of the phylogenetic tree
   * @param filename output filename
   * @throws IOException if file cannot be written
   */
  private void saveSimpleNewick(PhylogeneticNode root, String filename) 
      throws IOException {
    logger.info("Saving tree to {} (simple Newick format)", filename);
    
    String newickString = root.toNewickSimple() + ";";
    
    try (BufferedWriter writer = new BufferedWriter(new FileWriter(filename))) {
      writer.write(newickString);
      writer.newLine();
    }
    
    logger.info("Successfully saved simple Newick format to {}", filename);
  }
  
  /**
   * Saves the tree in Newick format with branch distances.
   *
   * @param root root of the phylogenetic tree
   * @param filename output filename
   * @throws IOException if file cannot be written
   */
  private void saveNewickWithDistances(PhylogeneticNode root, String filename) 
      throws IOException {
    logger.info("Saving tree to {} (Newick format with distances)", filename);
    
    String newickString = root.toNewickWithDistances() + ";";
    
    try (BufferedWriter writer = new BufferedWriter(new FileWriter(filename))) {
      writer.write(newickString);
      writer.newLine();
    }
    
    logger.info("Successfully saved Newick format with distances to {}", filename);
  }
  
  /**
   * Validates the Newick format string.
   *
   * @param newick the Newick string to validate
   * @return true if valid, false otherwise
   */
  public boolean validateNewickFormat(String newick) {
    if (newick == null || newick.isEmpty()) {
      return false;
    }
    
    // Basic validation: check parentheses balance and semicolon
    int openCount = 0;
    for (char c : newick.toCharArray()) {
      if (c == '(') openCount++;
      else if (c == ')') openCount--;
      if (openCount < 0) return false;
    }
    
    return openCount == 0 && newick.endsWith(";");
  }
}
