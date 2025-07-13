package com.phylogenetics.service;

import com.phylogenetics.model.TreeNode;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

/**
 * Exports phylogenetic tree to Newick format.
 */
public class NewickExporter {
    private static final String TREE_PREFIX = "./tree_blosum";
    private static final String NEWICK_SUFFIX = "_newick.nw";
    private static final String NEWICK_WITH_DISTANCE_SUFFIX = "_newick_with_distance.nw";

    public static void exportTree(TreeNode root, String blosumType) throws IOException {
        // Export basic Newick format (without distances)
        String basicNewick = toNewick(root, root, false);
        writeToFile(basicNewick, TREE_PREFIX + blosumType + NEWICK_SUFFIX);

        // Export Newick format with distances
        String newickWithDistances = toNewick(root, root, true);
        writeToFile(newickWithDistances, TREE_PREFIX + blosumType + NEWICK_WITH_DISTANCE_SUFFIX);
    }

    private static String toNewick(TreeNode node,TreeNode root, boolean includeDistances) {
        if (node.isLeaf()) {
            return includeDistances ? 
                String.format("%s:%d", node.getName(), (int)node.getHeight()) : 
                node.getName();
        }

        StringBuilder builder = new StringBuilder("(");
        for (int i = 0; i < node.getChildren().size(); i++) {
            if (i > 0) builder.append(",");
            builder.append(toNewick(node.getChildren().get(i),root,includeDistances));
        }
        builder.append(")");

        if (!node.isLeaf() && includeDistances) {
            builder.append(String.format(":%d", (int)node.getHeight()));
        }

        return builder.toString() + (node == root ? ";" : "");
    }

    private static void writeToFile(String content, String filePath) throws IOException {
        try (FileWriter writer = new FileWriter(filePath)) {
            writer.write(content);
        }
    }
}
