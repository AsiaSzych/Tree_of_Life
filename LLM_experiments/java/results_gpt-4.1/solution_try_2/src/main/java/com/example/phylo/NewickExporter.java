package com.example.phylo;

import java.io.FileWriter;
import java.io.IOException;

public class NewickExporter {

    /**
     * Exports the tree to Newick format (only leaf names).
     */
    public static void exportSimple(PhyloNode root, String filePath) throws IOException {
        String newick = toSimpleNewick(root) + ";";
        try (FileWriter writer = new FileWriter(filePath)) {
            writer.write(newick);
        }
    }

    private static String toSimpleNewick(PhyloNode node) {
        if (node.isLeaf()) {
            return node.getName();
        }
        return "(" + toSimpleNewick(node.getLeft()) + "," + toSimpleNewick(node.getRight()) + ")";
    }

    /**
     * Exports the tree to Newick format with integer branch lengths.
     * Branch length = parent height - child height (leaves have height 0).
     */
    public static void exportWithDistances(PhyloNode root, String filePath) throws IOException {
        String newick = toNewickWithDistances(root, root.getHeight()) + ";";
        try (FileWriter writer = new FileWriter(filePath)) {
            writer.write(newick);
        }
    }

    private static String toNewickWithDistances(PhyloNode node, int parentHeight) {
        if (node.isLeaf()) {
            int branchLength = parentHeight; // leaves: parentHeight - 0
            return node.getName() + ":" + branchLength;
        }
        int branchLengthLeft = parentHeight - node.getLeft().getHeight();
        int branchLengthRight = parentHeight - node.getRight().getHeight();
        String leftStr = toNewickWithDistances(node.getLeft(), node.getLeft().isLeaf() ? 0 : node.getLeft().getHeight());
        String rightStr = toNewickWithDistances(node.getRight(), node.getRight().isLeaf() ? 0 : node.getRight().getHeight());
        return "(" + leftStr + ":" + branchLengthLeft + "," + rightStr + ":" + branchLengthRight + ")";
    }
}