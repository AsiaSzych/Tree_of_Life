package com.phylo.util;

import com.phylo.model.PhyloNode;

public class NewickFormatter {

    public static String toNewickWithoutDistances(PhyloNode node) {
        if (node == null) return "";
        
        if (node.isLeaf()) {
            // Leaf node: return species name
            return node.getId();
        } else {
            // Internal node: recursively process children
            String left = toNewickWithoutDistances(node.getLeft());
            String right = toNewickWithoutDistances(node.getRight());
            return "(" + left + "," + right + ")";
        }
    }

    public static String toNewickWithDistances(PhyloNode node, double parentHeight) {
        if (node == null) return "";
        
        // Calculate branch length (difference in heights)
        double branchLength = parentHeight - node.getHeight();
        int intBranchLength = (int) branchLength;  // Convert to integer
        
        if (node.isLeaf()) {
            // Leaf node: species name and branch length
            return node.getId() + ":" + intBranchLength;
        } else {
            // Internal node: recursively process children
            String left = toNewickWithDistances(node.getLeft(), node.getHeight());
            String right = toNewickWithDistances(node.getRight(), node.getHeight());
            return "(" + left + "," + right + "):" + intBranchLength;
        }
    }
}