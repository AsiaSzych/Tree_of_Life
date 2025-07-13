package com.phylo.service;

import com.phylo.model.PhylogeneticNode;

public class NewickExporter {
    
    /**
     * Generates basic Newick format without distances
     */
    public static String toBasicNewick(PhylogeneticNode node) {
        if (node.isLeaf()) {
            return node.getName();
        } else {
            StringBuilder builder = new StringBuilder("(");
            for (int i = 0; i < node.getChildren().size(); i++) {
                if (i > 0) builder.append(",");
                builder.append(toBasicNewick(node.getChildren().get(i)));
            }
            builder.append(")");
            return builder.toString();
        }
    }

    /**
     * Generates Newick format with integer branch distances
     */
    public static String toDistanceNewick(PhylogeneticNode node) {
        return toDistanceNewick(node, node.getHeight());
    }

    private static String toDistanceNewick(PhylogeneticNode node, double parentHeight) {
        if (node.isLeaf()) {
            // Distance from parent to leaf = parent's height (since leaf height=0)
            return node.getName() + ":" + (int)parentHeight;
        } else {
            StringBuilder builder = new StringBuilder("(");
            for (int i = 0; i < node.getChildren().size(); i++) {
                if (i > 0) builder.append(",");
                // Distance = parent height - child height
                double distance = parentHeight - node.getChildren().get(i).getHeight();
                builder.append(toDistanceNewick(node.getChildren().get(i), node.getHeight()))
                      .append(":").append((int)distance);
            }
            builder.append(")");
            return builder.toString();
        }
    }
}