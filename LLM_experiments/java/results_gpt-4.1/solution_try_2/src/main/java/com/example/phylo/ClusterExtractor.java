package com.example.phylo;

import java.util.ArrayList;
import java.util.List;

public class ClusterExtractor {

    /**
     * Extracts clusters from the tree for a given threshold.
     * Each cluster is a list of species names (leaf nodes).
     */
    public static List<List<String>> extractClusters(PhyloNode root, int threshold) {
        List<List<String>> clusters = new ArrayList<>();
        extractClustersRecursive(root, threshold, clusters);
        return clusters;
    }

    private static void extractClustersRecursive(PhyloNode node, int threshold, List<List<String>> clusters) {
        if (node.isLeaf() || node.getHeight() <= threshold) {
            clusters.add(node.getLeafNames());
        } else {
            extractClustersRecursive(node.getLeft(), threshold, clusters);
            extractClustersRecursive(node.getRight(), threshold, clusters);
        }
    }
}