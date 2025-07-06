package com.phylo;

import com.phylo.model.PhyloNode;
import com.phylo.util.PhyloTreeUtils;
import com.phylo.util.UnionFind;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.HashMap;

public class ClusterFinder {
    
    public static List<List<String>> findClusters(
            PhyloNode root, List<String> species, int threshold) {
        // Precompute all pairs LCA scores
        Map<String, Map<String, Integer>> lcaScores = 
            PhyloTreeUtils.computeAllPairsLCA(root, species);
        
        // Initialize union-find
        int n = species.size();
        UnionFind uf = new UnionFind(n);
        Map<String, Integer> indexMap = createIndexMap(species);
        
        // Merge species based on LCA scores
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                String s1 = species.get(i);
                String s2 = species.get(j);
                int score = lcaScores.get(s1).get(s2);
                if (score >= threshold) {
                    uf.union(i, j);
                }
            }
        }
        
        return uf.getClusters(species);
    }

    private static Map<String, Integer> createIndexMap(List<String> species) {
        Map<String, Integer> map = new HashMap<>();
        for (int i = 0; i < species.size(); i++) {
            map.put(species.get(i), i);
        }
        return map;
    }
}