package com.phylogen.model;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.OptionalInt;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Represents a node in the phylogenetic tree.
 * A node can be a leaf (representing a single species) or an internal node
 * (representing a common ancestor of its children).
 */
public class TreeNode {

    private static final AtomicInteger idCounter = new AtomicInteger(0);
    private final int id;
    private final Optional<String> speciesName;
    private final OptionalInt similarityScore; // The score at which this node was formed by a merge
    private final List<TreeNode> children;

    // Constructor for a leaf node (a species)
    public TreeNode(String speciesName) {
        this.id = idCounter.getAndIncrement();
        this.speciesName = Optional.of(speciesName);
        this.children = Collections.emptyList();
        this.similarityScore = OptionalInt.empty(); // Leaves don't have a merge score
    }

    // Constructor for an internal node (a merge of children)
    public TreeNode(List<TreeNode> children, int similarityScore) {
        this.id = idCounter.getAndIncrement();
        this.speciesName = Optional.empty();
        this.children = Collections.unmodifiableList(new ArrayList<>(children));
        this.similarityScore = OptionalInt.of(similarityScore);
    }

    public int getId() {
        return id;
    }

    public Optional<String> getSpeciesName() {
        return speciesName;
    }

    public OptionalInt getSimilarityScore() {
        return similarityScore;
    }

    public List<TreeNode> getChildren() {
        return children;
    }

    public boolean isLeaf() {
        return children.isEmpty();
    }

    /**
     * Recursively finds all leaf node descendants of this node.
     * If this node is a leaf itself, it returns a list containing only this node.
     * @return A list of all terminal leaf nodes under this node.
     */
    public List<TreeNode> getLeafDescendants() {
        if (isLeaf()) {
            return Collections.singletonList(this);
        }
        List<TreeNode> leaves = new ArrayList<>();
        for (TreeNode child : children) {
            leaves.addAll(child.getLeafDescendants());
        }
        return leaves;
    }

    @Override
    public String toString() {
        if (isLeaf()) {
            return speciesName.orElse("Unknown Leaf");
        }
        return "InternalNode[score=" + similarityScore.orElseThrow() + ", children=" + children.size() + "]";
    }
}