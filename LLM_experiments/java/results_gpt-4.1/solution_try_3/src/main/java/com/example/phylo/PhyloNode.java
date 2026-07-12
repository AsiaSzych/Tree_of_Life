package com.example.phylo;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class PhyloNode {

  private final String name;
  private final List<PhyloNode> children;
  private final int height;

  public PhyloNode(String name) {
    this.name = name;
    this.children = Collections.emptyList();
    this.height = -1;
  }

  public PhyloNode(List<PhyloNode> children, int height) {
    this.name = null;
    this.children = new ArrayList<>(children);
    this.height = height;
  }

  public boolean isLeaf() {
    return children.isEmpty();
  }

  public String getName() {
    return name;
  }

  public List<PhyloNode> getChildren() {
    return Collections.unmodifiableList(children);
  }

  public int getHeight() {
    return height;
  }

  public List<String> getLeafNames() {
    List<String> leaves = new ArrayList<>();
    collectLeaves(this, leaves);
    return leaves;
  }

  private static void collectLeaves(PhyloNode node, List<String> leaves) {
    if (node.isLeaf()) {
      leaves.add(node.getName());
    } else {
      for (PhyloNode child : node.getChildren()) {
        collectLeaves(child, leaves);
      }
    }
  }
}