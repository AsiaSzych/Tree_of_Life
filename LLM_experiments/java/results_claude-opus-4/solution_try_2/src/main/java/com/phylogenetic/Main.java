package com.phylogenetic;

import com.phylogenetic.alignment.AlignmentService;
import com.phylogenetic.clustering.ClusteringService;
import com.phylogenetic.io.ClusterWriter;
import com.phylogenetic.io.DataLoader;
import com.phylogenetic.io.ThresholdLoader;
import com.phylogenetic.io.TreeWriter;
import com.phylogenetic.model.AlignmentResult;
import com.phylogenetic.model.BlosumMatrix;
import com.phylogenetic.model.Organism;
import com.phylogenetic.tree.PhylogeneticTree;
import com.phylogenetic.tree.PhylogeneticTreeBuilder;
import com.phylogenetic.visualization.DendrogramDrawer;
import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Main entry point for the phylogenetic analysis application.
 */
public class Main {
  private static final Logger LOGGER = Logger.getLogger(Main.class.getName());
  
  public static void main(String[] args) {
    try {
      // Determine which BLOSUM matrix to use
      String blosumFile = args.length > 0 ? args[0] : "blosum62.json";
      String blosumType = blosumFile.replaceAll(".*blosum(\\d+)\\.json", "$1");
      
      // Load data
      DataLoader loader = new DataLoader();
      List<Organism> organisms = loader.loadOrganisms("organisms.json");
      BlosumMatrix blosumMatrix = loader.loadBlosumMatrix(blosumFile);
      
      LOGGER.info("Loaded " + organisms.size() + " organisms");
      LOGGER.info("Using BLOSUM" + blosumType + " matrix");
      
      // Calculate alignments
      AlignmentService alignmentService = new AlignmentService(blosumMatrix);
      List<AlignmentResult> results = alignmentService.calculateAllPairwiseScores(organisms);
      
      LOGGER.info("Calculated " + results.size() + " pairwise alignments");
      
      // Convert results to map format for tree building
      Map<String, Integer> scoresMap = new HashMap<>();
      for (AlignmentResult result : results) {
        String key = result.organism1() + "_" + result.organism2();
        scoresMap.put(key, result.score());
      }
      
      // Build phylogenetic tree
      PhylogeneticTreeBuilder treeBuilder = new PhylogeneticTreeBuilder();
      PhylogeneticTree tree = treeBuilder.buildTree(organisms, scoresMap);
      
      LOGGER.info("Built phylogenetic tree with height: " + tree.getHeight());
      
      // Save tree in both Newick formats
      TreeWriter treeWriter = new TreeWriter();
      treeWriter.saveTreeFormats(tree, blosumType);
      
      // Draw dendrogram
      DendrogramDrawer dendrogramDrawer = new DendrogramDrawer(tree);
      String dendrogramFile = "phylogenetic_tree_blosum" + blosumType + ".png";
      dendrogramDrawer.drawToFile(dendrogramFile);
      LOGGER.info("Saved dendrogram to " + dendrogramFile);
      
      // Load thresholds and perform clustering
      ThresholdLoader thresholdLoader = new ThresholdLoader();
      List<Integer> thresholds = thresholdLoader.loadThresholds("thresholds.txt");
      
      if (!thresholds.isEmpty()) {
        // Calculate clusters
        ClusteringService clusteringService = new ClusteringService(tree);
        Map<Integer, List<List<String>>> clusteringResults = 
            clusteringService.calculateClustersForThresholds(thresholds);
        
        // Print results to console
        clusteringService.printClusteringResults(clusteringResults);
        
        // Save results to JSON
        ClusterWriter clusterWriter = new ClusterWriter();
        clusterWriter.saveClusteringResults(clusteringResults, blosumType);
      } else {
        LOGGER.warning("No thresholds found in thresholds.txt");
      }
      
    } catch (IOException e) {
      LOGGER.log(Level.SEVERE, "Error with file operations", e);
      System.exit(1);
    } catch (Exception e) {
      LOGGER.log(Level.SEVERE, "Unexpected error", e);
      System.exit(1);
    }
  }
}