package com.phylogenetic.tree;

import java.util.HashSet;
import java.util.Set;

/**
 * Represents a cluster of species during the agglomerative clustering process.
 */
public class Cluster {
  private final PhylogeneticNode node;
  private final Set<String> members;
  
  public Cluster(PhylogeneticNode node) {
    this.node = node;
    this.members = new HashSet<>(node.getLeafNames());
  }
  
  /**
   * Merge two clusters to create a new cluster.
   */
  public static Cluster merge(Cluster c1, Cluster c2, double similarity) {
    PhylogeneticNode newNode = new PhylogeneticNode(c1.getNode(), c2.getNode(), similarity);
    return new Cluster(newNode);
  }
  
  public PhylogeneticNode getNode() {
    return node;
  }
  
  public Set<String> getMembers() {
    return new HashSet<>(members);
  }
  
  public boolean contains(String species) {
    return members.contains(species);
  }
  
  public int size() {
    return members.size();
  }
}