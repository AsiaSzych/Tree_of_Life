package com.mycompany.phylogeny.algorithm;

import com.mycompany.phylogeny.domain.tree.InternalNode;
import com.mycompany.phylogeny.domain.tree.LeafNode;
import com.mycompany.phylogeny.domain.tree.TreeNode;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Objects;
import java.util.Set;
import java.util.stream.Collectors;

/**
 * Finds clusters of species from a phylogenetic tree based on a given similarity threshold.
 */
public class ClusterFinder {

  private final TreeNode root;

  public ClusterFinder(TreeNode root) {
    this.root = Objects.requireNonNull(root, "Root node cannot be null.");
  }

  /**
   * Calculates the clusters for a given similarity threshold.
   *
   * @param threshold The similarity score to "cut" the tree at.
   * @return A list of clusters, where each cluster is a list of species names.
   */
  public List<List<String>> findClusters(int threshold) {
    List<Set<String>> clustersAsSets = new ArrayList<>();
    findClustersRecursive(root, threshold, clustersAsSets);

    // Convert sets to sorted lists for consistent output
    return clustersAsSets.stream()
        .map(
            set -> {
              List<String> sortedList = new ArrayList<>(set);
              Collections.sort(sortedList);
              return sortedList;
            })
        .collect(Collectors.toList());
  }

  /**
   * The recursive helper method to traverse the tree and identify clusters.
   *
   * @param node The current node being evaluated.
   * @param threshold The similarity threshold.
   * @param clusters The list where discovered clusters are collected.
   */
  private void findClustersRecursive(TreeNode node, int threshold, List<Set<String>> clusters) {
    // If a node's merge height is at or above the threshold, all its descendants form one cluster.
    // We also check that it's an InternalNode, as LeafNodes have a height of 0.
    if (node instanceof InternalNode internalNode && internalNode.getHeight() >= threshold) {
      clusters.add(internalNode.getSpeciesNames());
      return; // Stop traversing this branch
    }

    // If the node is a leaf, it forms a cluster of its own.
    if (node instanceof LeafNode leafNode) {
      clusters.add(leafNode.getSpeciesNames());
      return;
    }

    // If the node is an internal node below the threshold, its merge is "cut".
    // We must continue searching for clusters in its children.
    if (node instanceof InternalNode internalNode) {
      findClustersRecursive(internalNode.getLeft(), threshold, clusters);
      findClustersRecursive(internalNode.getRight(), threshold, clusters);
    }
  }
}