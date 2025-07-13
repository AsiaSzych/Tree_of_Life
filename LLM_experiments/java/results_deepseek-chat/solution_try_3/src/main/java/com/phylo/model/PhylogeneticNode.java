package com.phylo.model;

import java.util.ArrayList;
import java.util.List;

/**
 * Represents a node in the phylogenetic tree (leaf or internal).
 */
public class PhylogeneticNode {
    private final String name;
    private final double height; // Needleman-Wunsch similarity score
    private final List<PhylogeneticNode> children;
    private final List<String> memberSpecies; // All species under this node

    public PhylogeneticNode(String name, double height) {
        this.name = name;
        this.height = height;
        this.children = new ArrayList<>();
        this.memberSpecies = new ArrayList<>();
        if (!name.startsWith("Internal_")) { // Leaf node
            this.memberSpecies.add(name);
        }
    }

    public void addChild(PhylogeneticNode child) {
        children.add(child);
        memberSpecies.addAll(child.getMemberSpecies());
    }

    // Getters
    public String getName() { return name; }
    public double getHeight() { return height; }
    public List<PhylogeneticNode> getChildren() { return children; }
    public List<String> getMemberSpecies() { return memberSpecies; }

    public boolean isLeaf() {
        return children.isEmpty();
    }
}