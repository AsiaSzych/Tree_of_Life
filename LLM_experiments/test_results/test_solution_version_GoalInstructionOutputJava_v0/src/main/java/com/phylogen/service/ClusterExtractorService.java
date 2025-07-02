package com.phylogen.service;

import com.phylogen.model.TreeNode;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Service to extract clusters of species from a phylogenetic tree based on a similarity threshold.
 */
public class ClusterExtractorService {

    /**
     * Finds all clusters in the tree for a given similarity threshold.
     *
     * @param root      The root node of the phylogenetic tree.
     * @param threshold The similarity score threshold.
     * @return A list of clusters, where each cluster is a list of species names.
     */
    public List<List<String>> findClustersForThreshold(TreeNode root, int threshold) {
        return findClustersRecursive(root, threshold);
    }

    /**
     * Recursively traverses the tree to identify clusters.
     *
     * @param node      The current node being evaluated.
     * @param threshold The similarity threshold.
     * @return A list of clusters found in the subtree of the current node.
     */
    private List<List<String>> findClustersRecursive(TreeNode node, int threshold) {
        // A node forms a single, coherent cluster if:
        // 1. It's a leaf node (a cluster of one).
        // 2. Its merge score is >= the threshold, meaning its members are "more similar" than required.
        if (node.isLeaf() || node.getSimilarityScore().orElse(Integer.MAX_VALUE) >= threshold) {
            List<String> cluster = node.getLeafDescendants().stream()
                    .map(leaf -> leaf.getSpeciesName().orElse("Unknown"))
                    .sorted() // Sort for consistent output
                    .collect(Collectors.toList());
            return List.of(cluster);
        }

        // If the node's score is below the threshold, its connection is "broken".
        // The final clusters are the combined results from its children.
        List<List<String>> allClusters = new ArrayList<>();
        for (TreeNode child : node.getChildren()) {
            allClusters.addAll(findClustersRecursive(child, threshold));
        }
        return allClusters;
    }
}