package com.phylo.service;

import com.phylo.model.ClusterNode;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

/**
 * Handles exporting phylogenetic trees to Newick format.
 */
public class NewickExporter {

    public static void exportToNewick(ClusterNode root, String blosumType) throws IOException {
        String basicNewick = buildBasicNewick(root);
        String withDistances = buildNewickWithDistances(root);

        saveToFile(basicNewick, "tree_blosum" + blosumType + "_newick.nw");
        saveToFile(withDistances, "tree_blosum" + blosumType + "_newick_with_distance.nw");
    }

    private static String buildBasicNewick(ClusterNode node) {
        if (node.isLeaf()) {
            return node.getLabel();
        }
        return "(" + buildBasicNewick(node.getLeft()) + "," + 
               buildBasicNewick(node.getRight()) + ")";
    }

    private static String buildNewickWithDistances(ClusterNode node) {
        if (node.isLeaf()) {
            return node.getLabel();
        }
        
        String leftStr = buildNewickWithDistances(node.getLeft());
        String rightStr = buildNewickWithDistances(node.getRight());
        
        // Calculate branch lengths (difference between node height and child height)
        int leftDist = (int) (node.getHeight() - node.getLeft().getHeight());
        int rightDist = (int) (node.getHeight() - node.getRight().getHeight());
        
        return "(" + leftStr + ":" + leftDist + "," + 
               rightStr + ":" + rightDist + ")";
    }

    private static void saveToFile(String content, String filename) throws IOException {
        try (FileWriter writer = new FileWriter("./" + filename)) {
            writer.write(content + ";");
        }
    }
}