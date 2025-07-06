package com.mycompany.phylogeny.domain.tree;

import java.util.Objects;
import java.util.Set;

/**
 * Represents a leaf node in the phylogenetic tree, corresponding to a single species.
 */
public final class LeafNode extends TreeNode {

  private final String speciesName;

  public LeafNode(String speciesName) {
    this.speciesName = Objects.requireNonNull(speciesName);
  }

  @Override
  public Set<String> getSpeciesNames() {
    return Set.of(speciesName);
  }

  @Override
  public int getHeight() {
    // A leaf node has no merge height. We return 0 as a baseline.
    // The height of interest is always on InternalNodes.
    return 0;
  }

  @Override
  public String toString() {
    return "Leaf(" + speciesName + ")";
  }

  // equals and hashCode are critical for using nodes in collections like Maps and Sets.
  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;
    LeafNode leafNode = (LeafNode) o;
    return speciesName.equals(leafNode.speciesName);
  }

  @Override
  public int hashCode() {
    return Objects.hash(speciesName);
  }
}