package com.example.phylo;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class PhyloNode {
    private final String name; // null for internal nodes
    private final PhyloNode left;
    private final PhyloNode right;
    private final int height; // Needleman-Wunsch similarity score at merge

    public PhyloNode(String name) {
        this.name = name;
        this.left = null;
        this.right = null;
        this.height = -1; // Not applicable for leaves
    }

    public PhyloNode(PhyloNode left, PhyloNode right, int height) {
        this.name = null;
        this.left = left;
        this.right = right;
        this.height = height;
    }

    public boolean isLeaf() {
        return name != null;
    }

    public String getName() {
        return name;
    }

    public PhyloNode getLeft() {
        return left;
    }

    public PhyloNode getRight() {
        return right;
    }

    public int getHeight() {
        return height;
    }

    public List<String> getLeafNames() {
        if (isLeaf()) {
            return Collections.singletonList(name);
        }
        List<String> names = new ArrayList<>();
        if (left != null) names.addAll(left.getLeafNames());
        if (right != null) names.addAll(right.getLeafNames());
        return names;
    }
}