package com.example.phylo;

import java.util.ArrayList;
import java.util.List;

public class ClusterFinder {

  /**
   * Returns a list of clusters (each cluster is a list of leaf names) for a given threshold.
   * Clusters are formed by cutting the tree at nodes with height >= threshold.
   */
  public static List<List<String>> findClusters(PhyloNode root, int threshold) {
    List<List<String>> clusters = new ArrayList<>();
    collectClusters(root, threshold, clusters);
    return clusters;
  }

  private static void collectClusters(PhyloNode node, int threshold, List<List<String>> clusters) {
    // If node is below threshold or is a leaf, it's a cluster root
    if (node.isLeaf() || node.getHeight() < threshold) {
      clusters.add(node.getLeafNames());
    } else {
      for (PhyloNode child : node.getChildren()) {
        collectClusters(child, threshold, clusters);
      }
    }
  }
}