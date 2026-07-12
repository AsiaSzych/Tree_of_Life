package com.phylogenetic;

import com.phylogenetic.alignment.AlignmentService;
import com.phylogenetic.alignment.AlignmentService.AlignmentData;
import com.phylogenetic.clustering.ClusteringService;
import com.phylogenetic.io.ClusterWriter;
import com.phylogenetic.io.NewickWriter;
import com.phylogenetic.tree.PhylogeneticNode;
import com.phylogenetic.tree.PhylogeneticTreeBuilder;
import com.phylogenetic.tree.TreeAnalyzer;
import com.phylogenetic.visualization.TreeVisualizer;
import java.io.IOException;
import java.util.List;
import java.util.Map;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Main service for phylogenetic analysis combining alignment and tree building.
 */
public class PhylogeneticAnalysis {
  private static final Logger logger = LoggerFactory.getLogger(PhylogeneticAnalysis.class);
  private final AlignmentService alignmentService;
  private final PhylogeneticTreeBuilder treeBuilder;
  private final TreeAnalyzer treeAnalyzer;
  private final NewickWriter newickWriter;
  private final TreeVisualizer treeVisualizer;
  private final ClusteringService clusteringService;
  private final ClusterWriter clusterWriter;
  
  public PhylogeneticAnalysis() {
    this.alignmentService = new AlignmentService();
    this.treeBuilder = new PhylogeneticTreeBuilder();
    this.treeAnalyzer = new TreeAnalyzer();
    this.newickWriter = new NewickWriter();
    this.treeVisualizer = new TreeVisualizer();
    this.clusteringService = new ClusteringService();
    this.clusterWriter = new ClusterWriter();
  }
  
  /**
   * Runs complete phylogenetic analysis.
   *
   * @param organismsFile path to organisms JSON file
   * @param blosumFile path to BLOSUM matrix file
   * @param thresholdsFile path to thresholds file (optional)
   * @return root of the phylogenetic tree
   * @throws IOException if files cannot be read
   */
  public PhylogeneticNode runAnalysis(
      String organismsFile, 
      String blosumFile,
      String thresholdsFile) throws IOException {
    
    logger.info("Starting phylogenetic analysis");
    
    // Get alignment data
    AlignmentData alignmentData = alignmentService.getAlignmentData(
        organismsFile, blosumFile);
    
    // Build phylogenetic tree
    PhylogeneticNode root = treeBuilder.buildTree(
        alignmentData.organisms(), 
        alignmentData.alignmentResults()
    );
    
    // Log tree summary
    logger.info("\n{}", treeAnalyzer.getTreeSummary(root));
    
    // Extract BLOSUM type
    String blosumType = extractBlosumType(blosumFile);
    
    // Save tree to Newick formats
    newickWriter.saveTree(root, blosumType);
    
    // Create visualizations
    treeVisualizer.visualizeTree(root, blosumType);
    
    // Process thresholds if file is provided
    if (thresholdsFile != null) {
      processThresholds(root, thresholdsFile, blosumType);
    }
    
    return root;
  }
  
  /**
   * Processes threshold-based clustering.
   *
   * @param root root of the phylogenetic tree
   * @param thresholdsFile path to thresholds file
   * @param blosumType BLOSUM matrix type
   * @throws IOException if files cannot be read/written
   */
  private void processThresholds(
      PhylogeneticNode root, 
      String thresholdsFile, 
      String blosumType) throws IOException {
    
    logger.info("Processing threshold-based clustering");
    
    // Read thresholds
    List<Integer> thresholds = clusteringService.readThresholds(thresholdsFile);
    
    if (thresholds.isEmpty()) {
      logger.warn("No valid thresholds found in {}", thresholdsFile);
      return;
    }
    
    // Generate clusters
    Map<Integer, List<List<String>>> clusters = 
        clusteringService.generateClusters(root, thresholds);
    
    // Save clusters to JSON
    clusterWriter.saveClusters(clusters, blosumType);
  }
  
  /**
   * Extracts BLOSUM type from filename.
   *
   * @param blosumFile filename of BLOSUM matrix
   * @return BLOSUM type (e.g., "BLOSUM50", "BLOSUM62")
   */
  private String extractBlosumType(String blosumFile) {
    return blosumFile.substring(0, blosumFile.lastIndexOf('.')).toUpperCase();
  }
}