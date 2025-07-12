package com.phylogenetic.tree;

import com.phylogenetic.model.Organism;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.logging.Logger;

/**
 * Builds a phylogenetic tree using agglomerative hierarchical clustering
 * with single linkage based on similarity scores.
 */
public class PhylogeneticTreeBuilder {
  private static final Logger LOGGER = Logger.getLogger(PhylogeneticTreeBuilder.class.getName());
  
  /**
   * Represents a pair of clusters with their similarity score.
   */
  private static class ClusterPair implements Comparable<ClusterPair> {
    final Cluster cluster1;
    final Cluster cluster2;
    final double similarity;
    
    ClusterPair(Cluster c1, Cluster c2, double similarity) {
      this.cluster1 = c1;
      this.cluster2 = c2;
      this.similarity = similarity;
    }
    
    @Override
    public int compareTo(ClusterPair other) {
      // Higher similarity should come first (max heap)
      return Double.compare(other.similarity, this.similarity);
    }
  }
  
  /**
   * Build a phylogenetic tree from organisms and their pairwise similarity scores.
   */
  public PhylogeneticTree buildTree(List<Organism> organisms, Map<String, Integer> scores) {
    LOGGER.info("Building phylogenetic tree for " + organisms.size() + " organisms");
    
    // Initialize clusters - each organism starts as its own cluster
    List<Cluster> activeClusters = new ArrayList<>();
    Map<String, Cluster> clusterMap = new HashMap<>();
    
    for (Organism organism : organisms) {
      PhylogeneticNode leafNode = new PhylogeneticNode(organism.name());
      Cluster cluster = new Cluster(leafNode);
      activeClusters.add(cluster);
      clusterMap.put(organism.name(), cluster);
    }
    
    // Build similarity matrix for efficient lookup
    Map<String, Map<String, Double>> similarityMatrix = buildSimilarityMatrix(scores);
    
    // Priority queue to always get the most similar pair
    PriorityQueue<ClusterPair> pairQueue = new PriorityQueue<>();
    
    // Initialize queue with all pairs
    for (int i = 0; i < activeClusters.size(); i++) {
      for (int j = i + 1; j < activeClusters.size(); j++) {
        Cluster c1 = activeClusters.get(i);
        Cluster c2 = activeClusters.get(j);
        double similarity = getSingleLinkageSimilarity(c1, c2, similarityMatrix);
        if (similarity > 0) {
          pairQueue.offer(new ClusterPair(c1, c2, similarity));
        }
      }
    }
    
    // Agglomerative clustering
    while (activeClusters.size() > 1) {
      // Find the most similar pair
      ClusterPair bestPair = null;
      while (!pairQueue.isEmpty()) {
        ClusterPair candidate = pairQueue.poll();
        // Check if both clusters are still active
        if (activeClusters.contains(candidate.cluster1) && 
            activeClusters.contains(candidate.cluster2)) {
          bestPair = candidate;
          break;
        }
      }
      
      if (bestPair == null) {
        throw new IllegalStateException("No valid cluster pairs found");
      }
      
      // Merge the clusters
      Cluster newCluster = Cluster.merge(bestPair.cluster1, bestPair.cluster2, 
                                         bestPair.similarity);
      
      LOGGER.fine("Merging clusters at similarity " + bestPair.similarity);
      
      // Update active clusters
      activeClusters.remove(bestPair.cluster1);
      activeClusters.remove(bestPair.cluster2);
      activeClusters.add(newCluster);
      
      // Add new pairs to queue
      for (Cluster other : activeClusters) {
        if (other != newCluster) {
          double similarity = getSingleLinkageSimilarity(newCluster, other, similarityMatrix);
          if (similarity > 0) {
            pairQueue.offer(new ClusterPair(newCluster, other, similarity));
          }
        }
      }
    }
    
    // The last remaining cluster contains the root node
    PhylogeneticNode root = activeClusters.get(0).getNode();
    LOGGER.info("Tree construction complete. Root height: " + root.getHeight());
    
    return new PhylogeneticTree(root);
  }
  
  /**
   * Build a similarity matrix from the scores map for efficient lookup.
   */
  private Map<String, Map<String, Double>> buildSimilarityMatrix(Map<String, Integer> scores) {
    Map<String, Map<String, Double>> matrix = new HashMap<>();
    
    for (Map.Entry<String, Integer> entry : scores.entrySet()) {
      String[] species = entry.getKey().split("_");
      if (species.length == 2) {
        matrix.computeIfAbsent(species[0], k -> new HashMap<>())
              .put(species[1], entry.getValue().doubleValue());
        matrix.computeIfAbsent(species[1], k -> new HashMap<>())
              .put(species[0], entry.getValue().doubleValue());
      }
    }
    
    return matrix;
  }
  
  /**
   * Calculate single linkage similarity between two clusters.
   * Single linkage uses the maximum similarity between any pair of species.
   */
  private double getSingleLinkageSimilarity(Cluster c1, Cluster c2, 
                                            Map<String, Map<String, Double>> similarityMatrix) {
    double maxSimilarity = 0;
    
    for (String species1 : c1.getMembers()) {
      for (String species2 : c2.getMembers()) {
        Double similarity = similarityMatrix.get(species1).get(species2);
        if (similarity != null && similarity > maxSimilarity) {
          maxSimilarity = similarity;
        }
      }
    }
    
    return maxSimilarity;
  }
}