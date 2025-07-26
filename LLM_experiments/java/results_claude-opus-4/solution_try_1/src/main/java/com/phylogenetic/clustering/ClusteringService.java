package com.phylogenetic.clustering;

import com.phylogenetic.io.DataLoader;
import com.phylogenetic.tree.PhylogeneticNode;
import com.phylogenetic.tree.TreeAnalyzer;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Service for threshold-based clustering of phylogenetic trees.
 */
public class ClusteringService {
  private static final Logger logger = LoggerFactory.getLogger(ClusteringService.class);
  private final TreeAnalyzer treeAnalyzer;
  
  public ClusteringService() {
    this.treeAnalyzer = new TreeAnalyzer();
  }
  
  /**
   * Reads threshold values from a file.
   *
   * @param filename path to thresholds file
   * @return list of threshold values
   * @throws IOException if file cannot be read
   */
  public List<Integer> readThresholds(String filename) throws IOException {
    logger.info("Reading thresholds from file: {}", filename);
    List<Integer> thresholds = new ArrayList<>();
    
    try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
      String line;
      while ((line = reader.readLine()) != null) {
        line = line.trim();
        if (!line.isEmpty()) {
          try {
            int threshold = Integer.parseInt(line);
            thresholds.add(threshold);
          } catch (NumberFormatException e) {
            logger.warn("Invalid threshold value: {}", line);
          }
        }
      }
    }
    
    logger.info("Read {} threshold values", thresholds.size());
    return thresholds;
  }
  
  /**
   * Generates clusters for all thresholds.
   *
   * @param root root of the phylogenetic tree
   * @param thresholds list of threshold values
   * @return map of threshold to clusters
   */
  public Map<Integer, List<List<String>>> generateClusters(
      PhylogeneticNode root, 
      List<Integer> thresholds) {
    
    logger.info("Generating clusters for {} thresholds", thresholds.size());
    Map<Integer, List<List<String>>> clusterMap = new TreeMap<>(); // TreeMap for sorted output
    
    for (Integer threshold : thresholds) {
      List<List<String>> clusters = treeAnalyzer.getClustersAtThreshold(root, threshold);
      clusterMap.put(threshold, clusters);
      
      logger.info("Threshold {}: {} clusters found", threshold, clusters.size());
      printClusters(threshold, clusters);
    }
    
    return clusterMap;
  }
  
  /**
   * Prints clusters to standard output.
   *
   * @param threshold the threshold value
   * @param clusters list of clusters
   */
  private void printClusters(int threshold, List<List<String>> clusters) {
    System.out.println("\n=== Clusters at threshold " + threshold + " ===");
    for (int i = 0; i < clusters.size(); i++) {
      System.out.println("Cluster " + (i + 1) + ": " + clusters.get(i));
    }
  }
}