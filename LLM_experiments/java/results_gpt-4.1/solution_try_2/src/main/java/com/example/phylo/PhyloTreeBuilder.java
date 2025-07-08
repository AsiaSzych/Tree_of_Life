package com.example.phylo;

import java.util.*;

public class PhyloTreeBuilder {

    /**
     * Builds a phylogenetic tree using single-linkage clustering on similarity scores.
     * @param similarityMatrix Map of (species1, species2) pairs to similarity scores.
     * @param speciesNames List of all species names.
     * @return Root node of the resulting phylogenetic tree.
     */
    public PhyloNode buildTree(SimilarityMatrix similarityMatrix, List<String> speciesNames) {
        // Initialize clusters: each species is its own cluster
        Map<String, PhyloNode> clusters = new HashMap<>();
        for (String name : speciesNames) {
            clusters.put(name, new PhyloNode(name));
        }

        // Track current cluster names for each cluster
        Map<Set<String>, PhyloNode> activeClusters = new HashMap<>();
        for (String name : speciesNames) {
            Set<String> singleton = new TreeSet<>();
            singleton.add(name);
            activeClusters.put(singleton, clusters.get(name));
        }

        while (activeClusters.size() > 1) {
            // Find the two clusters with the highest similarity
            int maxSim = Integer.MIN_VALUE;
            Set<String> bestA = null;
            Set<String> bestB = null;

            List<Set<String>> clusterList = new ArrayList<>(activeClusters.keySet());
            for (int i = 0; i < clusterList.size(); i++) {
                for (int j = i + 1; j < clusterList.size(); j++) {
                    Set<String> a = clusterList.get(i);
                    Set<String> b = clusterList.get(j);
                    int sim = getMaxSimilarity(similarityMatrix, a, b);
                    if (sim > maxSim) {
                        maxSim = sim;
                        bestA = a;
                        bestB = b;
                    }
                }
            }

            // Merge the two clusters
            Set<String> merged = new TreeSet<>();
            merged.addAll(bestA);
            merged.addAll(bestB);

            PhyloNode left = activeClusters.get(bestA);
            PhyloNode right = activeClusters.get(bestB);
            PhyloNode parent = new PhyloNode(left, right, maxSim);

            // Remove merged clusters and add new cluster
            activeClusters.remove(bestA);
            activeClusters.remove(bestB);
            activeClusters.put(merged, parent);
        }

        // Only one cluster remains: the root
        return activeClusters.values().iterator().next();
    }

    /**
     * Single-linkage: returns the maximum similarity between any member of clusterA and any member of clusterB.
     */
    private int getMaxSimilarity(SimilarityMatrix similarityMatrix, Set<String> clusterA, Set<String> clusterB) {
        int max = Integer.MIN_VALUE;
        for (String a : clusterA) {
            for (String b : clusterB) {
                if (!a.equals(b)) {
                    int sim = similarityMatrix.get(a, b);
                    if (sim > max) {
                        max = sim;
                    }
                }
            }
        }
        return max;
    }
}