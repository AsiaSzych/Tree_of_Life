package com.phylogenetic.clustering;

import com.phylogenetic.tree.PhylogeneticTree;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.logging.Logger;

/**
 * Service for performing threshold-based clustering on phylogenetic trees.
 */
public class ClusteringService {
  private static final Logger LOGGER = Logger.getLogger(ClusteringService.class.getName());
  
  private final PhylogeneticTree tree;
  
  public ClusteringService(PhylogeneticTree tree) {
    this.tree = tree;
  }
  
  /**
   * Calculate clusters for multiple thresholds.
   * 
   * @param thresholds List of threshold values
   * @return Map of threshold to list of clusters
   */
  public Map<Integer, List<List<String>>> calculateClustersForThresholds(List<Integer> thresholds) {
    Map<Integer, List<List<String>>> results = new HashMap<>();
    
    for (Integer threshold : thresholds) {
      List<List<String>> clusters = tree.getClustersAtThreshold(threshold.doubleValue());
      results.put(threshold, clusters);
      
      LOGGER.info("Threshold " + threshold + ": found " + clusters.size() + " clusters");
      
      // Log cluster details
      for (int i = 0; i < clusters.size(); i++) {
        LOGGER.fine("  Cluster " + (i + 1) + ": " + String.join(", ", clusters.get(i)));
      }
    }
    
    return results;
  }
  
  /**
   * Print clustering results to standard output.
   */
  public void printClusteringResults(Map<Integer, List<List<String>>> results) {
    System.out.println("\n=== CLUSTERING RESULTS ===");
    
    for (Map.Entry<Integer, List<List<String>>> entry : results.entrySet()) {
      Integer threshold = entry.getKey();
      List<List<String>> clusters = entry.getValue();
      
      System.out.println("\nThreshold: " + threshold);
      System.out.println("Number of clusters: " + clusters.size());
      
      for (int i = 0; i < clusters.size(); i++) {
        List<String> cluster = clusters.get(i);
        System.out.println("  Cluster " + (i + 1) + " (" + cluster.size() + " species): " + 
                          String.join(", ", cluster));
      }
    }
    
    System.out.println("\n=========================");
  }
}