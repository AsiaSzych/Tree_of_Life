package com.phylo.model;

import java.util.ArrayList;
import java.util.List;

/**
 * Represents a node in the phylogenetic tree (either leaf or internal node).
 */
public class ClusterNode {
    private final String label;
    private final double height; // Needleman-Wunsch score at merge
    private final ClusterNode left;
    private final ClusterNode right;
    private final List<String> members; // All species under this node

    // Constructor for leaf nodes (species)
    public ClusterNode(String species) {
        this.label = species;
        this.height = 0;
        this.left = null;
        this.right = null;
        this.members = new ArrayList<>();
        this.members.add(species);
    }

    // Constructor for internal nodes
    public ClusterNode(ClusterNode left, ClusterNode right, double height) {
        this.label = "Node_" + System.identityHashCode(this);
        this.height = height;
        this.left = left;
        this.right = right;
        this.members = new ArrayList<>();
        this.members.addAll(left.getMembers());
        this.members.addAll(right.getMembers());
    }

    // Getters
    public String getLabel() { return label; }
    public double getHeight() { return height; }
    public ClusterNode getLeft() { return left; }
    public ClusterNode getRight() { return right; }
    public List<String> getMembers() { return members; }

    public boolean isLeaf() {
        return left == null && right == null;
    }
}