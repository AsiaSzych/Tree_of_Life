package com.phylogenetic.tree;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

/**
 * Tests for PhylogeneticNode Newick format generation.
 */
class PhylogeneticNodeTest {
  
  @Test
  void testSimpleNewickFormat() {
    // Create a simple tree: (A,B,(C,D))
    PhylogeneticNode nodeA = new PhylogeneticNode("A");
    PhylogeneticNode nodeB = new PhylogeneticNode("B");
    PhylogeneticNode nodeC = new PhylogeneticNode("C");
    PhylogeneticNode nodeD = new PhylogeneticNode("D");
    
    PhylogeneticNode nodeCD = new PhylogeneticNode(nodeC, nodeD, 100);
    PhylogeneticNode root = new PhylogeneticNode(
        new PhylogeneticNode(nodeA, nodeB, 50), 
        nodeCD, 
        150
    );
    
    String newick = root.toNewickSimple();
    assertTrue(newick.contains("A"));
    assertTrue(newick.contains("B"));
    assertTrue(newick.contains("C"));
    assertTrue(newick.contains("D"));
    assertTrue(newick.contains("(") && newick.contains(")"));
  }
  
  @Test
  void testNewickWithDistances() {
    // Create a tree with specific heights
    PhylogeneticNode nodeA = new PhylogeneticNode("A");
    PhylogeneticNode nodeB = new PhylogeneticNode("B");
    
    PhylogeneticNode root = new PhylogeneticNode(nodeA, nodeB, 1200);
    
    String newick = root.toNewickWithDistances();
    assertTrue(newick.contains("A:1200"));
    assertTrue(newick.contains("B:1200"));
  }
}