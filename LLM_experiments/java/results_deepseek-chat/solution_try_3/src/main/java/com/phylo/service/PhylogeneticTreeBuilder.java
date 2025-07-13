package com.phylo.service;

import com.phylo.model.ClusterPair;
import com.phylo.model.PhylogeneticNode;
import com.phylo.util.Pair;

import java.util.*;

public class PhylogeneticTreeBuilder {
    private final Map<String, Integer> similarityScores;
    private int internalNodeCounter = 0;

    public PhylogeneticTreeBuilder(Map<Pair<String>, Integer> similarityScores) {
        this.similarityScores = convertToSingleKeyMap(similarityScores);
    }

    public PhylogeneticNode buildTree(Set<String> species) {
        // Initialize leaf nodes
        List<PhylogeneticNode> clusters = new ArrayList<>();
        for (String organism : species) {
            clusters.add(new PhylogeneticNode(organism, 0));
        }

        // Build priority queue of all possible pairs
        PriorityQueue<ClusterPair> queue = createClusterQueue(clusters);

        while (clusters.size() > 1) {
            ClusterPair bestPair = queue.poll();
            
            if (!clusters.contains(bestPair.cluster1()) || !clusters.contains(bestPair.cluster2())) {
                continue; // Skip if clusters were already merged
            }

            // Create new internal node
            PhylogeneticNode newNode = new PhylogeneticNode(
                "Internal_" + (++internalNodeCounter),
                bestPair.similarity()
            );
            newNode.addChild(bestPair.cluster1());
            newNode.addChild(bestPair.cluster2());

            // Remove merged clusters and add new node
            clusters.remove(bestPair.cluster1());
            clusters.remove(bestPair.cluster2());
            clusters.add(newNode);

            // Update queue with new possible pairs
            updateQueue(queue, clusters, newNode);
        }

        return clusters.get(0); // The root node
    }

    private PriorityQueue<ClusterPair> createClusterQueue(List<PhylogeneticNode> clusters) {
        PriorityQueue<ClusterPair> queue = new PriorityQueue<>();
        for (int i = 0; i < clusters.size(); i++) {
            for (int j = i + 1; j < clusters.size(); j++) {
                double similarity = getMaxSimilarity(clusters.get(i), clusters.get(j));
                queue.add(new ClusterPair(clusters.get(i), clusters.get(j), similarity));
            }
        }
        return queue;
    }

    private void updateQueue(PriorityQueue<ClusterPair> queue, 
                           List<PhylogeneticNode> clusters,
                           PhylogeneticNode newNode) {
        for (PhylogeneticNode existing : clusters) {
            if (existing != newNode) {
                double similarity = getMaxSimilarity(existing, newNode);
                queue.add(new ClusterPair(existing, newNode, similarity));
            }
        }
    }

    private double getMaxSimilarity(PhylogeneticNode a, PhylogeneticNode b) {
        double maxSimilarity = Integer.MIN_VALUE;
        for (String speciesA : a.getMemberSpecies()) {
            for (String speciesB : b.getMemberSpecies()) {
                String key = speciesA + "_" + speciesB;
                Integer similarity = similarityScores.get(key);
                if (similarity != null && similarity > maxSimilarity) {
                    maxSimilarity = similarity;
                }
            }
        }
        return maxSimilarity;
    }

    private Map<String, Integer> convertToSingleKeyMap(Map<Pair<String>, Integer> pairMap) {
        Map<String, Integer> result = new HashMap<>();
        pairMap.forEach((pair, score) -> 
            result.put(pair.first() + "_" + pair.second(), score));
        return result;
    }
}