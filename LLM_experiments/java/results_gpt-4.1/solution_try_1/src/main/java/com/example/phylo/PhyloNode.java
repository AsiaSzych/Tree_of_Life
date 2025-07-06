package com.example.phylo;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class PhyloNode {
  private final String name;
  private final PhyloNode left;
  private final PhyloNode right;
  private final int height;

  public PhyloNode(String name) {
    this.name = name;
    this.left = null;
    this.right = null;
    this.height = -1;
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

  public List<String> getAllSpecies() {
    if (isLeaf()) {
      return Collections.singletonList(name);
    }
    List<String> result = new ArrayList<>();
    result.addAll(left.getAllSpecies());
    result.addAll(right.getAllSpecies());
    return result;
  }
}