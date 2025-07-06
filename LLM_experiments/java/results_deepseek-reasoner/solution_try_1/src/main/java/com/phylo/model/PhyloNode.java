package com.phylo.model;

import java.util.Collections;
import java.util.List;

public class PhyloNode {
    private final String id;
    private final double height;
    private final PhyloNode left;
    private final PhyloNode right;
    private final List<String> species;

    // Constructor for leaf nodes
    public PhyloNode(String speciesName) {
        this.id = speciesName;
        this.height = 0.0;
        this.left = null;
        this.right = null;
        this.species = Collections.singletonList(speciesName);
    }

    // Constructor for internal nodes
    public PhyloNode(String id, double height, PhyloNode left, PhyloNode right) {
        this.id = id;
        this.height = height;
        this.left = left;
        this.right = right;
        this.species = combineSpecies(left, right);
    }

    private List<String> combineSpecies(PhyloNode left, PhyloNode right) {
        List<String> combined = new java.util.ArrayList<>(left.getSpecies());
        combined.addAll(right.getSpecies());
        return Collections.unmodifiableList(combined);
    }

    // Getters
    public String getId() { return id; }
    public double getHeight() { return height; }
    public PhyloNode getLeft() { return left; }
    public PhyloNode getRight() { return right; }
    public List<String> getSpecies() { return species; }
    public boolean isLeaf() { return left == null && right == null; }
}