package com.example.phylo;

import java.io.FileWriter;
import java.io.IOException;

public class NewickExporter {

  public static void exportSimple(PhyloNode root, String filePath) throws IOException {
    String newick = toNewickSimple(root) + ";";
    try (FileWriter writer = new FileWriter(filePath)) {
      writer.write(newick);
    }
  }

  private static String toNewickSimple(PhyloNode node) {
    if (node.isLeaf()) {
      return escapeName(node.getName());
    } else {
      return "(" + toNewickSimple(node.getLeft()) + "," + toNewickSimple(node.getRight()) + ")";
    }
  }

  public static void exportWithDistances(PhyloNode root, String filePath) throws IOException {
    String newick = toNewickWithDistances(root, root.getHeight()) + ";";
    try (FileWriter writer = new FileWriter(filePath)) {
      writer.write(newick);
    }
  }

  private static String toNewickWithDistances(PhyloNode node, int parentHeight) {
    if (node.isLeaf()) {
      int branchLength = parentHeight - 0;
      return escapeName(node.getName()) + ":" + branchLength;
    } else {
      int leftChildX = node.getLeft().isLeaf() ? 0 : node.getLeft().getHeight();
      int rightChildX = node.getRight().isLeaf() ? 0 : node.getRight().getHeight();
      String leftStr = toNewickWithDistances(node.getLeft(), node.getHeight());
      String rightStr = toNewickWithDistances(node.getRight(), node.getHeight());
      int branchLength = parentHeight - node.getHeight();
      return "(" + leftStr + "," + rightStr + ")" + ":" + branchLength;
    }
  }

  private static String escapeName(String name) {
    return name.replace(' ', '_');
  }
}