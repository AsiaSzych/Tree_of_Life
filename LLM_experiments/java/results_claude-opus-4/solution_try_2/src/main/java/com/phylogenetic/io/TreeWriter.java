package com.phylogenetic.io;

import com.phylogenetic.tree.PhylogeneticTree;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.logging.Logger;

/**
 * Handles writing phylogenetic trees to various file formats.
 */
public class TreeWriter {
  private static final Logger LOGGER = Logger.getLogger(TreeWriter.class.getName());
  
  /**
   * Save the phylogenetic tree in both Newick formats.
   * 
   * @param tree The phylogenetic tree to save
   * @param blosumType The BLOSUM matrix type used (e.g., "50" or "62")
   * @throws IOException if file writing fails
   */
  public void saveTreeFormats(PhylogeneticTree tree, String blosumType) throws IOException {
    // Save simple Newick format (without distances)
    String simpleFilename = "tree_blosum" + blosumType + "_newick.nw";
    saveNewickToFile(tree.toNewickSimple(), simpleFilename);
    LOGGER.info("Saved simple Newick format to " + simpleFilename);
    
    // Save Newick format with distances
    String distanceFilename = "tree_blosum" + blosumType + "_newick_with_distance.nw";
    saveNewickToFile(tree.toNewickWithDistances(), distanceFilename);
    LOGGER.info("Saved Newick format with distances to " + distanceFilename);
  }
  
  /**
   * Save a Newick string to a file.
   */
  private void saveNewickToFile(String newickString, String filename) throws IOException {
    Path path = Paths.get(filename);
    try (BufferedWriter writer = Files.newBufferedWriter(path)) {
      writer.write(newickString);
      writer.newLine();
    }
  }
  
  /**
   * Save only the simple Newick format.
   */
  public void saveSimpleNewick(PhylogeneticTree tree, String blosumType) throws IOException {
    String filename = "tree_blosum" + blosumType + "_newick.nw";
    saveNewickToFile(tree.toNewickSimple(), filename);
    LOGGER.info("Saved simple Newick format to " + filename);
  }
  
  /**
   * Save only the Newick format with distances.
   */
  public void saveNewickWithDistances(PhylogeneticTree tree, String blosumType) 
      throws IOException {
    String filename = "tree_blosum" + blosumType + "_newick_with_distance.nw";
    saveNewickToFile(tree.toNewickWithDistances(), filename);
    LOGGER.info("Saved Newick format with distances to " + filename);
  }
}