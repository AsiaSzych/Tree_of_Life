package com.mycompany.phylogeny.domain.tree;

import java.util.HashSet;
import java.util.Objects;
import java.util.Set;

/**
 * Represents an internal node in the phylogenetic tree, corresponding to a common ancestor.
 * It is formed by merging two child nodes (left and right).
 */
public final class InternalNode extends TreeNode {

  private final TreeNode left;
  private final TreeNode right;
  private final int height; // The similarity score at which this node was created.
  private final Set<String> speciesNames;

  public InternalNode(TreeNode left, TreeNode right, int height) {
    this.left = Objects.requireNonNull(left);
    this.right = Objects.requireNonNull(right);
    this.height = height;

    // Pre-calculate the set of species names for efficiency.
    Set<String> combinedNames = new HashSet<>(left.getSpeciesNames());
    combinedNames.addAll(right.getSpeciesNames());
    this.speciesNames = Set.copyOf(combinedNames);
  }

  public TreeNode getLeft() {
    return left;
  }

  public TreeNode getRight() {
    return right;
  }

  @Override
  public int getHeight() {
    return height;
  }

  @Override
  public Set<String> getSpeciesNames() {
    return speciesNames;
  }

  @Override
  public String toString() {
    return String.format("Internal(height=%d, species=%s)", height, speciesNames);
  }

  // equals and hashCode are important for correctness if used in collections.
  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;
    InternalNode that = (InternalNode) o;
    return height == that.height
        && left.equals(that.left)
        && right.equals(that.right);
  }

  @Override
  public int hashCode() {
    return Objects.hash(left, right, height);
  }
}