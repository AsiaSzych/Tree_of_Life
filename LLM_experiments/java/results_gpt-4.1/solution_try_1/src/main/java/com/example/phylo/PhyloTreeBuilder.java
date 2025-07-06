package com.example.phylo;

import java.util.*;

public class PhyloTreeBuilder {

  public static PhyloNode buildTree(List<String> speciesNames, SimilarityMatrix similarityMatrix) {
    List<PhyloNode> clusters = new ArrayList<>();
    for (String name : speciesNames) {
      clusters.add(new PhyloNode(name));
    }

    Map<PhyloNode, Set<String>> clusterSpecies = new HashMap<>();
    for (PhyloNode node : clusters) {
      clusterSpecies.put(node, new HashSet<>(Collections.singletonList(node.getName())));
    }

    while (clusters.size() > 1) {
      int maxSim = Integer.MIN_VALUE;
      int idxA = -1, idxB = -1;

      for (int i = 0; i < clusters.size(); i++) {
        for (int j = i + 1; j < clusters.size(); j++) {
          PhyloNode a = clusters.get(i);
          PhyloNode b = clusters.get(j);
          int sim = maxSimilarity(clusterSpecies.get(a), clusterSpecies.get(b), similarityMatrix);
          if (sim > maxSim) {
            maxSim = sim;
            idxA = i;
            idxB = j;
          }
        }
      }

      PhyloNode nodeA = clusters.get(idxA);
      PhyloNode nodeB = clusters.get(idxB);
      PhyloNode merged = new PhyloNode(nodeA, nodeB, maxSim);

      clusters.remove(idxB);
      clusters.remove(idxA);
      clusters.add(merged);

      Set<String> mergedSpecies = new HashSet<>();
      mergedSpecies.addAll(clusterSpecies.get(nodeA));
      mergedSpecies.addAll(clusterSpecies.get(nodeB));
      clusterSpecies.remove(nodeA);
      clusterSpecies.remove(nodeB);
      clusterSpecies.put(merged, mergedSpecies);
    }

    return clusters.get(0);
  }

  private static int maxSimilarity(Set<String> clusterA, Set<String> clusterB, SimilarityMatrix similarityMatrix) {
    int max = Integer.MIN_VALUE;
    for (String a : clusterA) {
      for (String b : clusterB) {
        if (!a.equals(b)) {
          Integer sim = similarityMatrix.get(a, b);
          if (sim != null && sim > max) {
            max = sim;
          }
        }
      }
    }
    return max;
  }
}