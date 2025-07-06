package com.phylo;

import com.phylo.model.Cluster;
import com.phylo.model.PhyloNode;
import com.phylo.util.SimilarityMatrixLoader;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.Deque;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;

public class PhylogeneticTreeBuilder {
    private final Map<String, Map<String, Integer>> similarityMatrix;
    private final List<String> species;
    private int internalNodeCounter = 0;

    public PhylogeneticTreeBuilder(Map<String, Map<String, Integer>> similarityMatrix, 
                                  List<String> species) {
        this.similarityMatrix = similarityMatrix;
        this.species = species;
    }

    public PhyloNode buildTree() {
        // Create initial clusters for each species
        List<Cluster> clusters = new ArrayList<>();
        for (String s : species) {
            clusters.add(new Cluster(new PhyloNode(s)));
        }

        // Continue merging until one cluster remains
        while (clusters.size() > 1) {
            // Find the two most similar clusters (single linkage)
            ClusterPair mostSimilar = findMostSimilarClusters(clusters);
            
            // Merge the two most similar clusters
            Cluster merged = mergeClusters(
                mostSimilar.cluster1, 
                mostSimilar.cluster2, 
                mostSimilar.similarity
            );
            
            // Update cluster list
            clusters.remove(mostSimilar.cluster1);
            clusters.remove(mostSimilar.cluster2);
            clusters.add(merged);
        }
        
        return clusters.get(0).getNode();
    }

    private ClusterPair findMostSimilarClusters(List<Cluster> clusters) {
        ClusterPair bestPair = null;
        double maxSimilarity = Double.NEGATIVE_INFINITY;
        
        for (int i = 0; i < clusters.size(); i++) {
            for (int j = i + 1; j < clusters.size(); j++) {
                Cluster c1 = clusters.get(i);
                Cluster c2 = clusters.get(j);
                
                double sim = getClusterSimilarity(c1, c2);
                if (sim > maxSimilarity) {
                    maxSimilarity = sim;
                    bestPair = new ClusterPair(c1, c2, sim);
                }
            }
        }
        
        return bestPair;
    }

    private double getClusterSimilarity(Cluster c1, Cluster c2) {
        // Single linkage: maximum similarity between any two species
        double maxSimilarity = Double.NEGATIVE_INFINITY;
        
        for (String s1 : c1.getSpecies()) {
            for (String s2 : c2.getSpecies()) {
                if (s1.equals(s2)) continue;
                
                Integer sim = similarityMatrix.get(s1).get(s2);
                if (sim != null && sim > maxSimilarity) {
                    maxSimilarity = sim;
                }
            }
        }
        
        return maxSimilarity;
    }

    private Cluster mergeClusters(Cluster c1, Cluster c2, double similarity) {
        internalNodeCounter++;
        String newId = "Internal_" + internalNodeCounter;
        
        PhyloNode newNode = new PhyloNode(
            newId, 
            similarity, 
            c1.getNode(), 
            c2.getNode()
        );
        
        return new Cluster(newNode);
    }

    // Helper class to store cluster pairs
    private static class ClusterPair {
        final Cluster cluster1;
        final Cluster cluster2;
        final double similarity;
        
        ClusterPair(Cluster cluster1, Cluster cluster2, double similarity) {
            this.cluster1 = cluster1;
            this.cluster2 = cluster2;
            this.similarity = similarity;
        }
    }
}