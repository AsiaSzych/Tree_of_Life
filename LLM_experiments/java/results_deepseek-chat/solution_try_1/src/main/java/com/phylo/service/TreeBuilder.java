package com.phylo.service;

import com.phylo.model.ClusterNode;
import com.phylo.util.Pair;
import java.util.*;

public class TreeBuilder {
    private final Map<String, Integer> similarityScores;

    public TreeBuilder(Map<String, Integer> similarityScores) {
        this.similarityScores = similarityScores;
    }

    public ClusterNode buildPhylogeneticTree(List<String> species) {
        // Initialize leaf nodes
        List<ClusterNode> clusters = new ArrayList<>();
        for (String specie : species) {
            clusters.add(new ClusterNode(specie));
        }

        // Create a lookup for cluster pairs
        Map<Pair<String>, Integer> scoreLookup = new HashMap<>();
        similarityScores.forEach((key, score) -> {
            String[] parts = key.split("_");
            scoreLookup.put(new Pair<>(parts[0], parts[1]), score);
        });

        // Hierarchical clustering
        while (clusters.size() > 1) {
            // Find the two most similar clusters
            ClusterPair bestPair = findMostSimilarClusters(clusters, scoreLookup);
            
            // Merge them
            ClusterNode newNode = new ClusterNode(
                bestPair.node1(),
                bestPair.node2(),
                bestPair.similarity()
            );
            
            clusters.remove(bestPair.node1());
            clusters.remove(bestPair.node2());
            clusters.add(newNode);
        }

        return clusters.get(0); // The root node
    }

    private ClusterPair findMostSimilarClusters(
            List<ClusterNode> clusters,
            Map<Pair<String>, Integer> scoreLookup) {
        double maxSimilarity = Double.NEGATIVE_INFINITY;
        ClusterNode bestNode1 = null, bestNode2 = null;

        for (int i = 0; i < clusters.size(); i++) {
            for (int j = i + 1; j < clusters.size(); j++) {
                ClusterNode node1 = clusters.get(i);
                ClusterNode node2 = clusters.get(j);
                
                double currentSimilarity = calculateSingleLinkageSimilarity(
                    node1, node2, scoreLookup);
                
                if (currentSimilarity > maxSimilarity) {
                    maxSimilarity = currentSimilarity;
                    bestNode1 = node1;
                    bestNode2 = node2;
                }
            }
        }

        return new ClusterPair(bestNode1, bestNode2, maxSimilarity);
    }

    private double calculateSingleLinkageSimilarity(
            ClusterNode node1,
            ClusterNode node2,
            Map<Pair<String>, Integer> scoreLookup) {
        double maxSimilarity = Double.NEGATIVE_INFINITY;
        
        for (String member1 : node1.getMembers()) {
            for (String member2 : node2.getMembers()) {
                Integer similarity = scoreLookup.get(new Pair<>(member1, member2));
                if (similarity != null && similarity > maxSimilarity) {
                    maxSimilarity = similarity;
                }
            }
        }
        
        return maxSimilarity;
    }

    private record ClusterPair(ClusterNode node1, ClusterNode node2, double similarity) {}
}