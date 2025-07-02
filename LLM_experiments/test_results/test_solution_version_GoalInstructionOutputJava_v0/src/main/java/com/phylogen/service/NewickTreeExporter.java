package com.phylogen.service;

import com.phylogen.model.TreeNode;

import java.util.Map;
import java.util.stream.Collectors;

/**
 * Service to export a phylogenetic tree (TreeNode) to the Newick format.
 */
public class NewickTreeExporter {

    /**
     * Exports the tree to a simple Newick format string (e.g., "(A,B,(C,D));").
     *
     * @param root The root node of the tree.
     * @return The Newick format string.
     */
    public String toSimpleNewick(TreeNode root) {
        return toNewickRecursive(root, null, 0, false) + ";";
    }

    /**
     * Exports the tree to a Newick format string with branch lengths (distances).
     * E.g., "(A:1,B:2,(C:D):3);"
     *
     * @param root             The root node of the tree.
     * @param similarityScores The map of scores, used to find the max similarity for leaf branch lengths.
     * @return The Newick format string with distances.
     */
    public String toNewickWithDistances(TreeNode root, Map<String, Map<String, Integer>> similarityScores) {
        int maxSimilarity = findMaxSimilarity(similarityScores);
        return toNewickRecursive(root, null, maxSimilarity, true) + ";";
    }

    /**
     * Recursive helper function to build the Newick string.
     *
     * @param node             The current node to process.
     * @param parentScore      The similarity score of the parent node. Null for the root.
     * @param maxSimilarity    The overall maximum similarity score, used as the "height" of leaves.
     * @param withDistances    Flag to include branch lengths.
     * @return A partial Newick string for the subtree rooted at 'node'.
     */
    private String toNewickRecursive(TreeNode node, Integer parentScore, int maxSimilarity, boolean withDistances) {
        // Base case: a leaf node
        if (node.isLeaf()) {
            String leafName = node.getSpeciesName().orElse("Unknown");
            if (withDistances) {
                // Branch length is the difference between the parent's merge score and the max score.
                int branchLength = maxSimilarity - parentScore;
                return String.format("%s:%d", leafName, branchLength);
            }
            return leafName;
        }

        // Recursive step: an internal node
        String childrenStr = node.getChildren().stream()
                .map(child -> toNewickRecursive(child, node.getSimilarityScore().orElseThrow(), maxSimilarity, withDistances))
                .collect(Collectors.joining(","));

        String result = String.format("(%s)", childrenStr);

        if (withDistances && parentScore != null) {
            // Branch length is the difference between the parent's score and this node's score.
            int branchLength = Math.abs(parentScore - node.getSimilarityScore().orElseThrow());
            result += ":" + branchLength;
        }

        return result;
    }

    /**
     * Finds the maximum similarity score from the entire score matrix.
     */
    private int findMaxSimilarity(Map<String, Map<String, Integer>> scores) {
        return scores.values().stream()
                .flatMap(innerMap -> innerMap.values().stream())
                .max(Integer::compareTo)
                .orElseThrow(() -> new IllegalArgumentException("Similarity scores map cannot be empty."));
    }
}