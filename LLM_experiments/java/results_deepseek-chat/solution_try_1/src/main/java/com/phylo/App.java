package com.phylo;

import com.phylo.model.ClusterNode;
import com.phylo.model.Organisms;
import com.phylo.service.AlignmentService;
import com.phylo.service.FileService;
import com.phylo.service.NewickExporter;
import com.phylo.service.TreeBuilder;
import com.phylo.service.ClusterFinder;
import com.phylo.service.DendrogramExporter;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class App {
    private static final String ORGANISMS_FILE = "./organisms.json";
    private static final String BLOSUM_TYPE = "62"; // or "50"
    private static final int DEFAULT_GAP_PENALTY = -4;

    public static void main(String[] args) {
        try {
            // 1. Load data and calculate scores
            Organisms organisms = FileService.readOrganisms(ORGANISMS_FILE);
            AlignmentService alignmentService = new AlignmentService(
                FileService.readBlosumMatrix("./blosum" + BLOSUM_TYPE + ".json", DEFAULT_GAP_PENALTY)
            );
            Map<String, Integer> scores = alignmentService.calculateAndSaveAllPairs(organisms, BLOSUM_TYPE);

            // 2. Build phylogenetic tree
            TreeBuilder treeBuilder = new TreeBuilder(scores);
            ClusterNode root = treeBuilder.buildPhylogeneticTree(
                new ArrayList<>(organisms.speciesMap().keySet())
            );

            // 3. Export to Newick format
            NewickExporter.exportToNewick(root, BLOSUM_TYPE);

            System.out.println("Phylogenetic tree built and exported successfully");
            
            DendrogramExporter.exportDendrogram(root, BLOSUM_TYPE);
            Map<Integer, List<List<String>>> clusters = 
            ClusterFinder.findClustersForThresholds(root, "./thresholds.txt", BLOSUM_TYPE);

            // Print results to console
            System.out.println("\nCluster Results:");
            clusters.forEach((threshold, clusterList) -> {
                System.out.println("\nThreshold: " + threshold);
                for (int i = 0; i < clusterList.size(); i++) {
                    System.out.println("Cluster " + (i+1) + ": " + clusterList.get(i));
                }
            });
        } catch (IOException e) {
            System.err.println("Error: " + e.getMessage());
        }
    }
}