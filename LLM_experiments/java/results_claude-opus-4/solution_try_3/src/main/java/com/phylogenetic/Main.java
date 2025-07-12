package com.phylogenetic;

import com.phylogenetic.alignment.NeedlemanWunsch;
import com.phylogenetic.alignment.PairwiseAlignmentCalculator;
import com.phylogenetic.clustering.ClusterCalculator;
import com.phylogenetic.config.ApplicationConfig;
import com.phylogenetic.io.ClusterWriter;
import com.phylogenetic.io.DataLoader;
import com.phylogenetic.io.NewickWriter;
import com.phylogenetic.io.ResultWriter;
import com.phylogenetic.io.ScoreLoader;
import com.phylogenetic.io.ThresholdLoader;
import com.phylogenetic.model.BlosumMatrix;
import com.phylogenetic.model.Organism;
import com.phylogenetic.tree.PhylogeneticTree;
import com.phylogenetic.tree.TreeBuilder;
import com.phylogenetic.visualization.DendrogramDrawer;
import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Map;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Main entry point for the phylogenetic analysis application.
 */
public class Main {
  private static final Logger logger = LoggerFactory.getLogger(Main.class);

  public static void main(String[] args) {
    // Determine which BLOSUM matrix to use (default to 50 if not specified)
    String blosumType = args.length > 0 ? args[0] : "50";
    
    if (!blosumType.equals("50") && !blosumType.equals("62")) {
      logger.error("Invalid BLOSUM type: {}. Must be 50 or 62.", blosumType);
      System.exit(1);
    }
    
    ApplicationConfig config = ApplicationConfig.createDefault(blosumType);
    String scoresFile = String.format("organisms_scores_blosum%s.json", blosumType);
    
    try {
      // Check if scores file exists
      if (!new File(scoresFile).exists()) {
        logger.info("Scores file not found. Calculating alignments...");
        calculateAndSaveAlignments(config, blosumType);
      }
      
      // Load scores and build tree
      logger.info("Loading scores and building phylogenetic tree...");
      ScoreLoader scoreLoader = new ScoreLoader();
      Map<String, Map<String, Integer>> scoreMatrix = scoreLoader.loadScores(scoresFile);
      
      TreeBuilder treeBuilder = new TreeBuilder();
      PhylogeneticTree tree = treeBuilder.buildTree(scoreMatrix);
      
      // Save tree in Newick formats
      NewickWriter newickWriter = new NewickWriter();
      newickWriter.saveTree(tree, blosumType);
      
      // Draw dendrogram
      String dendrogramFile = String.format("phylogenetic_tree_blosum%s.png", 
          blosumType);
      DendrogramDrawer drawer = new DendrogramDrawer();
      drawer.drawDendrogram(tree, dendrogramFile);
      
      // Check if thresholds file exists
      String thresholdsFile = "thresholds.txt";
      if (new File(thresholdsFile).exists()) {
        logger.info("Processing clustering with thresholds...");
        
        // Load thresholds
        ThresholdLoader thresholdLoader = new ThresholdLoader();
        List<Integer> thresholds = thresholdLoader.loadThresholds(thresholdsFile);
        
        // Calculate clusters
        ClusterCalculator calculator = new ClusterCalculator();
        Map<Integer, List<List<String>>> clusterResults = 
            calculator.calculateClustersForThresholds(tree, thresholds);
        
        // Print results
        calculator.printClusters(clusterResults);
        
        // Save results
        ClusterWriter clusterWriter = new ClusterWriter();
        clusterWriter.saveClusters(clusterResults, blosumType);
      } else {
        logger.info("No thresholds.txt file found. Skipping clustering analysis.");
      }
      
      // Print summary
      logger.info("\n=== ANALYSIS COMPLETE ===");
      logger.info("Results saved:");
      logger.info("  - Alignment scores: {}", scoresFile);
      logger.info("  - Tree (simple): tree_blosum{}_newick.nw", blosumType);
      logger.info("  - Tree (with distances): tree_blosum{}_newick_with_distance.nw", 
          blosumType);
      logger.info("  - Dendrogram: {}", dendrogramFile);
      if (new File(thresholdsFile).exists()) {
        logger.info("  - Clusters: clusters_for_blosum{}.json", blosumType);
      }
      logger.info("Tree statistics:");
      logger.info("  - Species count: {}", tree.getAllSpecies().size());
      logger.info("  - Score range: {} to {}", tree.getMinScore(), tree.getMaxScore());
      
    } catch (IOException e) {
      logger.error("Error with file operations", e);
      System.exit(1);
    } catch (Exception e) {
      logger.error("Unexpected error", e);
      System.exit(1);
    }
  }
  
  private static void calculateAndSaveAlignments(ApplicationConfig config, 
      String blosumType) throws IOException {
    // Load data
    DataLoader loader = new DataLoader();
    List<Organism> organisms = loader.loadOrganisms(config.getOrganismsFile());
    BlosumMatrix blosumMatrix = loader.loadBlosumMatrix(config.getBlosumFile());
    
    // Calculate pairwise alignments
    NeedlemanWunsch aligner = new NeedlemanWunsch(blosumMatrix);
    PairwiseAlignmentCalculator calculator = new PairwiseAlignmentCalculator(aligner);
    
    Map<String, Map<String, Integer>> scoreMatrix = 
        calculator.calculateAllPairwiseScores(organisms);
    
    // Save results to file
    ResultWriter writer = new ResultWriter();
    writer.saveScores(scoreMatrix, blosumMatrix.getMatrixType());
  }
}