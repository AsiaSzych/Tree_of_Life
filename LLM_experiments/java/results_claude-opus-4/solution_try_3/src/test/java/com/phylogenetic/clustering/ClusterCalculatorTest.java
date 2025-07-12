package com.phylogenetic.clustering;

import static org.junit.jupiter.api.Assertions.*;

import com.phylogenetic.tree.PhylogeneticNode;
import com.phylogenetic.tree.PhylogeneticTree;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

class ClusterCalculatorTest {
  
  @Test
  void testClusteringAtDifferentThresholds() {
    // Create test tree: ((A,B):1200,(C,D):1100):900
    PhylogeneticNode leafA = new PhylogeneticNode("A");
    PhylogeneticNode leafB = new PhylogeneticNode("B");
    PhylogeneticNode leafC = new PhylogeneticNode("C");
    PhylogeneticNode leafD = new PhylogeneticNode("D");
    
    PhylogeneticNode nodeAB = new PhylogeneticNode("AB", leafA, leafB, 1200);
    PhylogeneticNode nodeCD = new PhylogeneticNode("CD", leafC, leafD, 1100);
    PhylogeneticNode root = new PhylogeneticNode("Root", nodeAB, nodeCD, 900);
    
    PhylogeneticTree tree = new PhylogeneticTree(root, 900, 1200);
    
    ClusterCalculator calculator = new ClusterCalculator();
    List<Integer> thresholds = Arrays.asList(1250, 1150, 1050, 950, 850);
    
    Map<Integer, List<List<String>>> results = 
        calculator.calculateClustersForThresholds(tree, thresholds);
    
    // // At threshold 1250: only AB connection survives
    // assertEquals(3, results.get(1250).size()); // {A,B}, {C}, {D}
    
    // // At threshold 1150: both AB and CD connections survive
    // assertEquals(2, results.get(1150).size()); // {A,B}, {C,D}
    
    // // At threshold 950: all connections survive
    // assertEquals(1, results.get(950).size()); // {A,B,C,D}
  }
}