package com.phylogenetic.tree;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for PhylogeneticTree Newick format generation.
 */
public class PhylogeneticTreeTest {
  
  @Test
  public void testSimpleNewickFormat() {
    // Create a simple tree: ((A,B),C)
    PhylogeneticNode leafA = new PhylogeneticNode("A");
    PhylogeneticNode leafB = new PhylogeneticNode("B");
    PhylogeneticNode leafC = new PhylogeneticNode("C");
    
    PhylogeneticNode internalAB = new PhylogeneticNode(leafA, leafB, 100.0);
    PhylogeneticNode root = new PhylogeneticNode(internalAB, leafC, 200.0);
    
    PhylogeneticTree tree = new PhylogeneticTree(root);
    
    String expected = "((A,B),C);";
    assertEquals(expected, tree.toNewickSimple());
  }
  
  @Test
  public void testNewickWithDistances() {
    // Create a simple tree with specific heights
    PhylogeneticNode leafA = new PhylogeneticNode("A");
    PhylogeneticNode leafB = new PhylogeneticNode("B");
    PhylogeneticNode leafC = new PhylogeneticNode("C");
    
    PhylogeneticNode internalAB = new PhylogeneticNode(leafA, leafB, 1200.0);
    PhylogeneticNode root = new PhylogeneticNode(internalAB, leafC, 1500.0);
    
    PhylogeneticTree tree = new PhylogeneticTree(root);
    
    String newick = tree.toNewickWithDistances();
    assertTrue(newick.contains(":1200")); // Branch length to A and B
    assertTrue(newick.contains(":300"));  // Branch length from AB to root
    assertTrue(newick.contains(":1500")); // Branch length to C
  }
}