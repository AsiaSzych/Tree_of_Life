package com.mycompany.phylogeny.domain.tree;

import java.util.Set;

/**
 * Abstract base class for a node in the phylogenetic tree.
 * Each node, whether a leaf or internal, can report the set of species it contains.
 */
public abstract class TreeNode {

  /**
   * Gets the set of all species names contained within this node and its descendants.
   *
   * @return An immutable set of species names.
   */
  public abstract Set<String> getSpeciesNames();

  /**
   * Gets the height of the node, which corresponds to the similarity score
   * at which this node was formed. Not applicable for LeafNodes.
   *
   * @return The height of the node.
   */
  public abstract int getHeight();
}