package com.mycompany.phylogeny.algorithm;

import com.mycompany.phylogeny.domain.Species;
import com.mycompany.phylogeny.domain.tree.InternalNode;
import com.mycompany.phylogeny.domain.tree.LeafNode;
import com.mycompany.phylogeny.domain.tree.TreeNode;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import smile.clustering.HierarchicalClustering;

/**
 * Builds a phylogenetic tree using an agglomerative hierarchical clustering algorithm.
 * It produces both a custom TreeNode structure and a Smile-compatible data structure.
 */
public class HierarchicalClusterer {

  /**
   * Builds the tree and returns a result object containing our custom tree and Smile plot data.
   */
  public ClusteringResult buildTree(
      List<Species> speciesList, Map<String, Map<String, Integer>> similarityScores) {

    int n = speciesList.size();
    List<TreeNode> activeClusters = new ArrayList<>();
    Map<TreeNode, Integer> clusterIndices = new HashMap<>();

    // 1. Initialize leaf nodes and their initial indices (0 to n-1)
    for (int i = 0; i < n; i++) {
      LeafNode leaf = new LeafNode(speciesList.get(i).name());
      activeClusters.add(leaf);
      clusterIndices.put(leaf, i);
    }

    // Data structures for Smile's HierarchicalClustering
    int[] merge = new int[n - 1];
    double[] height = new double[n - 1];
    int mergeIndex = 0;

    while (activeClusters.size() > 1) {
      ClusterPair bestPair = findMostSimilarPair(activeClusters, similarityScores);

      int index1 = clusterIndices.get(bestPair.cluster1());
      int index2 = clusterIndices.get(bestPair.cluster2());

      // Record the merge for Smile. The new cluster's index will be n + mergeIndex.
      merge[mergeIndex] = index1;
      merge[mergeIndex + (n - 1)] = index2; // Smile stores merges in a flat array
      height[mergeIndex] = bestPair.similarity();

      // Create our custom internal node
      InternalNode newNode =
          new InternalNode(bestPair.cluster1(), bestPair.cluster2(), bestPair.similarity());

      // Update active clusters and their indices
      activeClusters.remove(bestPair.cluster1());
      activeClusters.remove(bestPair.cluster2());
      activeClusters.add(newNode);
      clusterIndices.put(newNode, n + mergeIndex);

      mergeIndex++;
    }

    HierarchicalClustering smileHc = new HierarchicalClustering(merge, height);
    TreeNode rootNode = activeClusters.get(0);

    return new ClusteringResult(rootNode, smileHc);
  }

  private ClusterPair findMostSimilarPair(
      List<TreeNode> clusters, Map<String, Map<String, Integer>> scores) {
    if (clusters.size() < 2) {
      throw new IllegalArgumentException("Cannot find a pair in a list with fewer than 2 clusters.");
    }
    TreeNode bestCluster1 = null;
    TreeNode bestCluster2 = null;
    int maxSimilarity = Integer.MIN_VALUE;
    for (int i = 0; i < clusters.size(); i++) {
      for (int j = i + 1; j < clusters.size(); j++) {
        TreeNode c1 = clusters.get(i);
        TreeNode c2 = clusters.get(j);
        int currentSimilarity = calculateClusterSimilarity(c1, c2, scores);
        if (currentSimilarity > maxSimilarity) {
          maxSimilarity = currentSimilarity;
          bestCluster1 = c1;
          bestCluster2 = c2;
        }
      }
    }
    return new ClusterPair(bestCluster1, bestCluster2, maxSimilarity);
  }

  private int calculateClusterSimilarity(
      TreeNode c1, TreeNode c2, Map<String, Map<String, Integer>> scores) {
    Set<String> species1 = c1.getSpeciesNames();
    Set<String> species2 = c2.getSpeciesNames();
    int maxSimilarity = Integer.MIN_VALUE;
    for (String s1 : species1) {
      for (String s2 : species2) {
        String outerKey = s1.compareTo(s2) < 0 ? s1 : s2;
        String innerKey = s1.compareTo(s2) < 0 ? s2 : s1;
        Integer score = scores.getOrDefault(outerKey, Map.of()).get(innerKey);
        if (score != null && score > maxSimilarity) {
          maxSimilarity = score;
        }
      }
    }
    return maxSimilarity;
  }

  private record ClusterPair(TreeNode cluster1, TreeNode cluster2, int similarity) {}
}