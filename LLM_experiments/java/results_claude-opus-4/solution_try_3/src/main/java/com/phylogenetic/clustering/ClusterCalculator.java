package com.phylogenetic.clustering;

import com.phylogenetic.tree.PhylogeneticTree;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Calculates clusters of species based on similarity thresholds.
 */
public class ClusterCalculator {
  private static final Logger logger = LoggerFactory.getLogger(ClusterCalculator.class);
  
  /**
   * Calculate clusters for multiple thresholds.
   * 
   * @param tree The phylogenetic tree
   * @param thresholds List of threshold values
   * @return Map of threshold to list of clusters
   */
  public Map<Integer, List<List<String>>> calculateClustersForThresholds(
      PhylogeneticTree tree, List<Integer> thresholds) {
    
    // Use TreeMap for sorted output
    Map<Integer, List<List<String>>> results = new TreeMap<>();
    
    for (Integer threshold : thresholds) {
      logger.info("Calculating clusters for threshold: {}", threshold);
      
      try {
        List<List<String>> clusters = tree.getClustersAtThreshold(threshold);
        results.put(threshold, clusters);
        
        logger.info("Found {} clusters at threshold {}", clusters.size(), threshold);
        
        // Log cluster details
        for (int i = 0; i < clusters.size(); i++) {
          logger.debug("  Cluster {}: {} species - {}", 
              i + 1, clusters.get(i).size(), clusters.get(i));
        }
        
      } catch (IllegalArgumentException e) {
        logger.warn("Invalid threshold {}: {}", threshold, e.getMessage());
        // Add empty cluster list for invalid thresholds
        results.put(threshold, new ArrayList<>());
      }
    }
    
    return results;
  }
  
  /**
   * Print clusters to standard output in a readable format.
   */
  public void printClusters(Map<Integer, List<List<String>>> clusterResults) {
    System.out.println("\n=== CLUSTERING RESULTS ===\n");
    
    for (Map.Entry<Integer, List<List<String>>> entry : clusterResults.entrySet()) {
      Integer threshold = entry.getKey();
      List<List<String>> clusters = entry.getValue();
      
      System.out.printf("Threshold: %d%n", threshold);
      System.out.printf("Number of clusters: %d%n", clusters.size());
      
      for (int i = 0; i < clusters.size(); i++) {
        List<String> cluster = clusters.get(i);
        System.out.printf("  Cluster %d (%d species): %s%n", 
            i + 1, cluster.size(), String.join(", ", cluster));
      }
      
      System.out.println();
    }
  }
}