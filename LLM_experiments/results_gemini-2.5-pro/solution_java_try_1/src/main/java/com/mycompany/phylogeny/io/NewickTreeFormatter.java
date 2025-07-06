package com.mycompany.phylogeny.io;

import com.mycompany.phylogeny.domain.tree.InternalNode;
import com.mycompany.phylogeny.domain.tree.LeafNode;
import com.mycompany.phylogeny.domain.tree.TreeNode;
import java.util.Objects;

/**
 * Formats a phylogenetic tree (TreeNode) into the Newick standard format.
 */
public class NewickTreeFormatter {

  /**
   * Formats the tree into a simple Newick string without branch lengths.
   * Example: (A,B,(C,D));
   *
   * @param root The root node of the tree.
   * @return The Newick format string.
   */
  public String formatSimple(TreeNode root) {
    Objects.requireNonNull(root, "Root node cannot be null.");
    return buildNewickString(root, root.getHeight(), false) + ";";
  }

  /**
   * Formats the tree into a Newick string including integer branch lengths.
   * Example: (A:1,B:2,(C:3,D:4):5);
   *
   * @param root The root node of the tree.
   * @return The Newick format string with distances.
   */
  public String formatWithDistances(TreeNode root) {
    Objects.requireNonNull(root, "Root node cannot be null.");
    return buildNewickString(root, root.getHeight(), true) + ";";
  }

  /**
   * Recursively builds the Newick string for a given node.
   *
   * @param node The current node to process.
   * @param parentHeight The height of the parent node, used to calculate branch length.
   * @param includeDistances True to include branch lengths, false otherwise.
   * @return The partial Newick string for the current node.
   */
  private String buildNewickString(TreeNode node, int parentHeight, boolean includeDistances) {
    if (node instanceof LeafNode leaf) {
      // A leaf node is just its name.
      String name = leaf.getSpeciesNames().iterator().next();
      if (includeDistances) {
        int branchLength = parentHeight - leaf.getHeight(); // height is 0 for leaves
        return name + ":" + branchLength;
      }
      return name;
    }

    if (node instanceof InternalNode internal) {
      // An internal node is a combination of its children.
      String leftStr = buildNewickString(internal.getLeft(), internal.getHeight(), includeDistances);
      String rightStr =
          buildNewickString(internal.getRight(), internal.getHeight(), includeDistances);
      String combined = "(" + leftStr + "," + rightStr + ")";

      if (includeDistances) {
        // The root node has no parent, so its branch length is not displayed.
        // We check this by seeing if its parent's height is its own height.
        if (parentHeight != internal.getHeight()) {
          int branchLength = parentHeight - internal.getHeight();
          return combined + ":" + branchLength;
        }
      }
      return combined;
    }

    // Should not be reached with the current sealed hierarchy.
    throw new IllegalStateException("Unknown TreeNode type: " + node.getClass().getName());
  }
}