package com.mycompany.phylogeny.algorithm;

import com.mycompany.phylogeny.domain.tree.TreeNode;
import smile.clustering.HierarchicalClustering;

/**
 * A wrapper for the results of the hierarchical clustering process.
 *
 * @param rootNode The root of our custom phylogenetic tree structure.
 * @param smileHc The clustering data in a format compatible with the Smile library for plotting.
 */
public record ClusteringResult(TreeNode rootNode, HierarchicalClustering smileHc) {}
