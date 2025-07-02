package com.phylogen.service;

import com.phylogen.model.Species;
import com.phylogen.model.TreeNode;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Objects;

/**
 * Service to build a phylogenetic tree using agglomerative hierarchical clustering.
 * It uses the "single linkage" method based on maximum similarity.
 */
public class HierarchicalClusteringService {

    private final List<Species> speciesList;
    private final Map<String, Map<String, Integer>> similarityScores;

    public HierarchicalClusteringService(List<Species> speciesList, Map<String, Map<String, Integer>> similarityScores) {
        this.speciesList = speciesList;
        this.similarityScores = similarityScores;
    }

    /**
     * Builds the phylogenetic tree.
     * @return The root node of the completed tree.
     */
    public TreeNode buildTree() {
        // 1. Initialize each species as a separate cluster (leaf node)
        List<TreeNode> activeClusters = new ArrayList<>();
        for (Species species : speciesList) {
            activeClusters.add(new TreeNode(species.name()));
        }

        // 2. Iteratively merge clusters until only one remains (the root)
        while (activeClusters.size() > 1) {
            MergeCandidate bestMerge = findBestPairToMerge(activeClusters);

            // Create a new internal node representing the merge
            TreeNode mergedNode = new TreeNode(
                    List.of(bestMerge.node1, bestMerge.node2),
                    bestMerge.similarity
            );

            // Remove the old clusters and add the new merged one
            activeClusters.remove(bestMerge.node1);
            activeClusters.remove(bestMerge.node2);
            activeClusters.add(mergedNode);
        }

        // The last remaining cluster is the root of the tree
        return activeClusters.get(0);
    }

    /**
     * Finds the pair of clusters in the active set with the highest similarity.
     */
    private MergeCandidate findBestPairToMerge(List<TreeNode> activeClusters) {
        TreeNode bestNode1 = null;
        TreeNode bestNode2 = null;
        int maxSimilarity = Integer.MIN_VALUE;

        for (int i = 0; i < activeClusters.size(); i++) {
            for (int j = i + 1; j < activeClusters.size(); j++) {
                TreeNode node1 = activeClusters.get(i);
                TreeNode node2 = activeClusters.get(j);

                int currentSimilarity = calculateClusterSimilarity(node1, node2);

                if (currentSimilarity > maxSimilarity) {
                    maxSimilarity = currentSimilarity;
                    bestNode1 = node1;
                    bestNode2 = node2;
                }
            }
        }
        return new MergeCandidate(bestNode1, bestNode2, maxSimilarity);
    }

    /**
     * Calculates the similarity between two clusters (nodes) using the single-linkage criterion.
     * For similarity, this means finding the MAXIMUM similarity between any two leaves from the respective clusters.
     */
    private int calculateClusterSimilarity(TreeNode cluster1, TreeNode cluster2) {
        int maxScore = Integer.MIN_VALUE;
        List<TreeNode> leaves1 = cluster1.getLeafDescendants();
        List<TreeNode> leaves2 = cluster2.getLeafDescendants();

        for (TreeNode leaf1 : leaves1) {
            for (TreeNode leaf2 : leaves2) {
                // We can safely call .get() because leaf nodes always have a species name
                String name1 = leaf1.getSpeciesName().get();
                String name2 = leaf2.getSpeciesName().get();
                int score = similarityScores.get(name1).get(name2);
                if (score > maxScore) {
                    maxScore = score;
                }
            }
        }
        return maxScore;
    }

    // A private record to hold the result of the search for the best pair to merge.
    private record MergeCandidate(TreeNode node1, TreeNode node2, int similarity) {
        MergeCandidate {
            Objects.requireNonNull(node1);
            Objects.requireNonNull(node2);
        }
    }
}