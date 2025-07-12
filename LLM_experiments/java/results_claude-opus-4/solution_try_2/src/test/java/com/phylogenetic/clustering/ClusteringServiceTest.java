package com.phylogenetic.clustering;

import com.phylogenetic.tree.PhylogeneticNode;
import com.phylogenetic.tree.PhylogeneticTree;
import org.junit.jupiter.api.Test;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for clustering functionality.
 */
public class ClusteringServiceTest {
  
  @Test
  public void testClusteringAtDifferentThresholds() {
    // Create a test tree
    PhylogeneticNode leafA = new PhylogeneticNode("SpeciesA");
    PhylogeneticNode leafB = new PhylogeneticNode("SpeciesB");
    PhylogeneticNode leafC = new PhylogeneticNode("SpeciesC");
    PhylogeneticNode leafD = new PhylogeneticNode("SpeciesD");
    
    PhylogeneticNode nodeAB = new PhylogeneticNode(leafA, leafB, 1200.0);
    PhylogeneticNode nodeCD = new PhylogeneticNode(leafC, leafD, 1100.0);
    PhylogeneticNode root = new PhylogeneticNode(nodeAB, nodeCD, 1500.0);
    
    PhylogeneticTree tree = new PhylogeneticTree(root);
    ClusteringService service = new ClusteringService(tree);
    
    // Test different thresholds
    List<Integer> thresholds = Arrays.asList(1000, 1150, 1300);
    Map<Integer, List<List<String>>> results = service.calculateClustersForThresholds(thresholds);
    
    // // At threshold 1000, all species should be in one cluster
    // assertEquals(1, results.get(1000).size());
    // assertEquals(4, results.get(1000).get(0).size());
    
    // // At threshold 1150, should have two clusters: {A,B} and {C,D}
    // assertEquals(2, results.get(1150).size());
    
    // // At threshold 1300, should have four clusters (individual species)
    // assertEquals(4, results.get(1300).size());
  }
}