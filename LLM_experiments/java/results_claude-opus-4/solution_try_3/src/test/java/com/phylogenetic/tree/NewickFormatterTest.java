package com.phylogenetic.tree;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

class NewickFormatterTest {
  
  @Test
  void testSimpleNewickFormat() {
    // Create a simple tree: ((A,B),C)
    PhylogeneticNode leafA = new PhylogeneticNode("A");
    PhylogeneticNode leafB = new PhylogeneticNode("B");
    PhylogeneticNode leafC = new PhylogeneticNode("C");
    
    PhylogeneticNode internalAB = new PhylogeneticNode("AB", leafA, leafB, 100);
    PhylogeneticNode root = new PhylogeneticNode("Root", internalAB, leafC, 50);
    
    NewickFormatter formatter = new NewickFormatter();
    String newick = formatter.toNewickSimple(root);
    
    assertEquals("((A,B),C);", newick);
  }
  
  @Test
  void testNewickWithDistances() {
    // Create a tree with specific heights
    PhylogeneticNode leafA = new PhylogeneticNode("A");
    PhylogeneticNode leafB = new PhylogeneticNode("B");
    PhylogeneticNode leafC = new PhylogeneticNode("C");
    PhylogeneticNode leafD = new PhylogeneticNode("D");
    
    // Internal nodes with heights
    PhylogeneticNode nodeAB = new PhylogeneticNode("AB", leafA, leafB, 1200);
    PhylogeneticNode nodeCD = new PhylogeneticNode("CD", leafC, leafD, 1100);
    PhylogeneticNode root = new PhylogeneticNode("Root", nodeAB, nodeCD, 800);
    
    NewickFormatter formatter = new NewickFormatter();
    String newick = formatter.toNewickWithDistances(root);
    
    // Should have format like ((A:1200,B:1200):400,(C:1100,D:1100):300);
    assertTrue(newick.contains("A:1200"));
    assertTrue(newick.contains("B:1200"));
    assertTrue(newick.contains("C:1100"));
    assertTrue(newick.contains("D:1100"));
    assertTrue(newick.endsWith(";"));
  }
}