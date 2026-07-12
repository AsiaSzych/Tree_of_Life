package com.example.phylo;

import java.util.*;

public class PhyloTreeBuilder {

  public PhyloNode buildTree(Map<String, Integer> similarityScores, Set<String> species) {
    Map<Set<String>, PhyloNode> clusters = new HashMap<>();
    for (String s : species) {
      Set<String> singleton = Collections.singleton(s);
      clusters.put(singleton, new PhyloNode(s));
    }

    List<Set<String>> clusterKeys = new ArrayList<>(clusters.keySet());

    while (clusters.size() > 1) {
      int maxSim = Integer.MIN_VALUE;
      Set<String> bestA = null;
      Set<String> bestB = null;

      for (int i = 0; i < clusterKeys.size(); i++) {
        for (int j = i + 1; j < clusterKeys.size(); j++) {
          Set<String> clusterA = clusterKeys.get(i);
          Set<String> clusterB = clusterKeys.get(j);

          int bestPairSim = Integer.MIN_VALUE;
          for (String leafA : clusterA) {
            for (String leafB : clusterB) {
              String key = leafA.compareTo(leafB) < 0
                  ? leafA + "_" + leafB
                  : leafB + "_" + leafA;
              Integer sim = similarityScores.get(key);
              if (sim != null && sim > bestPairSim) {
                bestPairSim = sim;
              }
            }
          }
          if (bestPairSim > maxSim) {
            maxSim = bestPairSim;
            bestA = clusterA;
            bestB = clusterB;
          }
        }
      }

      if (bestA == null || bestB == null) {
        throw new IllegalStateException("Could not find clusters to merge. Check similarity scores.");
      }

      Set<String> merged = new HashSet<>();
      merged.addAll(bestA);
      merged.addAll(bestB);

      List<PhyloNode> children = new ArrayList<>();
      children.add(clusters.get(bestA));
      children.add(clusters.get(bestB));
      PhyloNode parent = new PhyloNode(children, maxSim);

      clusters.remove(bestA);
      clusters.remove(bestB);
      clusterKeys.remove(bestA);
      clusterKeys.remove(bestB);

      clusters.put(merged, parent);
      clusterKeys.add(merged);
    }

    return clusters.values().iterator().next();
  }
}