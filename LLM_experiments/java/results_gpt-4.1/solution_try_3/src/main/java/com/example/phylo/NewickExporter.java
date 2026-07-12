package com.example.phylo;

import java.util.List;

public class NewickExporter {

  public static String toNewick(PhyloNode node) {
    StringBuilder sb = new StringBuilder();
    buildNewick(node, sb, false, 0);
    sb.append(';');
    return sb.toString();
  }

  public static String toNewickWithDistances(PhyloNode node) {
    StringBuilder sb = new StringBuilder();
    buildNewick(node, sb, true, node.getHeight());
    sb.append(';');
    return sb.toString();
  }

  private static void buildNewick(PhyloNode node, StringBuilder sb, boolean withDistances, int parentHeight) {
    if (node.isLeaf()) {
      sb.append(escapeName(node.getName()));
      if (withDistances) {
        int branchLength = parentHeight - node.getHeight();
        sb.append(':').append(branchLength);
      }
    } else {
      List<PhyloNode> children = node.getChildren();
      sb.append('(');
      for (int i = 0; i < children.size(); i++) {
        buildNewick(children.get(i), sb, withDistances, node.getHeight());
        if (i < children.size() - 1) {
          sb.append(',');
        }
      }
      sb.append(')');
      if (withDistances && parentHeight != node.getHeight()) {
        int branchLength = parentHeight - node.getHeight();
        sb.append(':').append(branchLength);
      }
    }
  }

  private static String escapeName(String name) {
    if (name.matches("[A-Za-z0-9_]+")) {
      return name;
    }
    return "'" + name.replace("'", "''") + "'";
  }
}
