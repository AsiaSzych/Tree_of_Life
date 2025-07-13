package com.phylogenetics.service;

import com.phylogenetics.model.TreeNode;
import java.util.*;

/**
 * Builds phylogenetic tree using single-linkage hierarchical clustering.
 */
public class TreeBuilder {
    public TreeNode buildTree(Map<String, Integer> similarityScores, List<String> species) {
        // Initialize leaf nodes
        List<TreeNode> clusters = new ArrayList<>();
        Map<String, TreeNode> clusterMap = new HashMap<>();
        for (String organism : species) {
            TreeNode node = new TreeNode(organism, Double.POSITIVE_INFINITY);
            clusters.add(node);
            clusterMap.put(organism, node);
        }

        // Create a working copy of similarity scores
        Map<String, Integer> scores = new HashMap<>(similarityScores);

        while (clusters.size() > 1) {
            // Find the pair with maximum similarity
            String maxPair = null;
            int maxScore = Integer.MIN_VALUE;

            for (Map.Entry<String, Integer> entry : scores.entrySet()) {
                if (entry.getValue() > maxScore) {
                    maxScore = entry.getValue();
                    maxPair = entry.getKey();
                }
            }

            if (maxPair == null) break;

            // Split pair into two species
            String[] parts = maxPair.split("_");
            String species1 = parts[0];
            String species2 = parts[1];

            // Find clusters containing these species
            TreeNode cluster1 = findCluster(clusters, species1);
            TreeNode cluster2 = findCluster(clusters, species2);

            // Create new internal node
            TreeNode newNode = new TreeNode(maxScore, cluster1, cluster2);

            // Update cluster list
            clusters.remove(cluster1);
            clusters.remove(cluster2);
            clusters.add(newNode);

            // Update similarity scores for new cluster
            scores = updateScores(scores, clusters, newNode);
        }

        return clusters.get(0); // The root node
    }

    private TreeNode findCluster(List<TreeNode> clusters, String species) {
        for (TreeNode node : clusters) {
            if (node.getMembers().contains(species)) {
                return node;
            }
        }
        throw new IllegalArgumentException("Species not found in any cluster: " + species);
    }

    private Map<String, Integer> updateScores(
            Map<String, Integer> oldScores,
            List<TreeNode> clusters,
            TreeNode newNode) {
        Map<String, Integer> newScores = new HashMap<>();

        // Single linkage: new cluster's similarity = max similarity with any member
        for (TreeNode cluster : clusters) {
            if (cluster != newNode) {
                int maxSimilarity = Integer.MIN_VALUE;
                for (String member1 : newNode.getMembers()) {
                    for (String member2 : cluster.getMembers()) {
                        String key1 = member1 + "_" + member2;
                        String key2 = member2 + "_" + member1;
                        int similarity = oldScores.getOrDefault(key1, 
                            oldScores.getOrDefault(key2, Integer.MIN_VALUE));
                        if (similarity > maxSimilarity) {
                            maxSimilarity = similarity;
                        }
                    }
                }
                if (maxSimilarity != Integer.MIN_VALUE) {
                    String newKey = newNode.getMembers().get(0) + "_" + cluster.getMembers().get(0);
                    newScores.put(newKey, maxSimilarity);
                }
            }
        }

        return newScores;
    }
}