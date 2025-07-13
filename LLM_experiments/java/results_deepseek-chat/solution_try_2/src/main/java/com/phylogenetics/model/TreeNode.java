package com.phylogenetics.model;

import java.util.ArrayList;
import java.util.List;

/**
 * Represents a node in the phylogenetic tree (leaf or internal).
 */
public class TreeNode {
    private final String name;
    private final double height; // Needleman-Wunsch similarity score at merge
    private final List<TreeNode> children;
    private final List<String> members; // All leaf species under this node

    public TreeNode(String name, double height) {
        this.name = name;
        this.height = height;
        this.children = new ArrayList<>();
        this.members = new ArrayList<>();
        this.members.add(name);
    }

    // For internal nodes
    public TreeNode(double height, TreeNode child1, TreeNode child2) {
        this.name = "Node_" + System.currentTimeMillis();
        this.height = height;
        this.children = new ArrayList<>();
        this.children.add(child1);
        this.children.add(child2);
        this.members = new ArrayList<>();
        this.members.addAll(child1.getMembers());
        this.members.addAll(child2.getMembers());
    }

    // Getters
    public String getName() { return name; }
    public double getHeight() { return height; }
    public List<TreeNode> getChildren() { return children; }
    public List<String> getMembers() { return members; }

    public boolean isLeaf() {
        return children.isEmpty();
    }
}