package com.phylo.util;

import com.phylo.model.PhyloNode;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class PhyloTreeUtils {

    public static Map<String, Map<String, Integer>> computeAllPairsLCA(
            PhyloNode root, List<String> species) {
        Map<String, Map<String, Integer>> lcaMatrix = new HashMap<>();
        for (String s1 : species) {
            lcaMatrix.put(s1, new HashMap<>());
            for (String s2 : species) {
                if (!s1.equals(s2)) {
                    PhyloNode lca = findLCA(root, s1, s2);
                    lcaMatrix.get(s1).put(s2, (int) lca.getHeight());
                }
            }
        }
        return lcaMatrix;
    }

    private static PhyloNode findLCA(PhyloNode root, String species1, String species2) {
        if (root == null) return null;
        if (root.isLeaf() && (root.getId().equals(species1) || root.getId().equals(species2))) {
            return root;
        }
        
        PhyloNode left = findLCA(root.getLeft(), species1, species2);
        PhyloNode right = findLCA(root.getRight(), species1, species2);
        
        if (left != null && right != null) return root;
        return left != null ? left : right;
    }
}