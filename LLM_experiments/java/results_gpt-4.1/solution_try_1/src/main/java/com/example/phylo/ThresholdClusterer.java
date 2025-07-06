package com.example.phylo;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class ThresholdClusterer {

  public static Map<Integer, List<List<String>>> getClustersForThresholds(PhyloNode root, List<Integer> thresholds) {
    Map<Integer, List<List<String>>> result = new HashMap<>();
    for (int threshold : thresholds) {
      List<List<String>> clusters = new ArrayList<>();
      collectClusters(root, threshold, clusters);
      result.put(threshold, clusters);
    }
    return result;
  }

  private static void collectClusters(PhyloNode node, int threshold, List<List<String>> clusters) {
    if (node.isLeaf() || node.getHeight() < threshold) {
      clusters.add(node.getAllSpecies());
    } else {
      collectClusters(node.getLeft(), threshold, clusters);
      collectClusters(node.getRight(), threshold, clusters);
    }
  }
}