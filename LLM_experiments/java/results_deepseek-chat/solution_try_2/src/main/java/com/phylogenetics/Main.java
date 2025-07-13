package com.phylogenetics;

import com.phylogenetics.model.*;
import com.phylogenetics.service.*;

import java.io.IOException;
import java.util.*;

public class Main {
    private static final String ORGANISMS_FILE = "./organisms.json";
    private static final String BLOSUM_FILE_PREFIX = "./blosum";
    private static final String BLOSUM_FILE_SUFFIX = ".json";

    public static void main(String[] args) {
        if (args.length < 1) {
            System.err.println("Usage: java Main <blosum_type>");
            System.err.println("Example: java Main 62");
            return;
        }

        String blosumType = args[0];
        String blosumFile = BLOSUM_FILE_PREFIX + blosumType + BLOSUM_FILE_SUFFIX;

        try {
            // Load data
            Map<String, Organism> organisms = FileParser.parseOrganisms(ORGANISMS_FILE);
            SubstitutionMatrix matrix = FileParser.parseSubstitutionMatrix(blosumFile);
            
            // Calculate alignment scores
            AlignmentService alignmentService = new AlignmentService(matrix);
            Map<String, Map<String, Integer>> scores = alignmentService.calculateAllPairs(organisms);
            
            // Save results to file
            ResultWriter.writeResults(scores, blosumType);
            
            // Build phylogenetic tree
            Map<String, Integer> flatScores = flattenScores(scores);
            TreeBuilder treeBuilder = new TreeBuilder();
            TreeNode root = treeBuilder.buildTree(flatScores, new ArrayList<>(organisms.keySet()));
            
            // Export to Newick format
            NewickExporter.exportTree(root, blosumType);
            
            // Draw dendrogram
            // DendrogramDrawer.drawDendrogram(root, blosumType);
            
            // Find and save clusters
            ClusterFinder.findAndSaveClusters(root, blosumType);
            
            System.out.println("Pipeline completed successfully!");
            
        } catch (IOException e) {
            System.err.println("Error processing files: " + e.getMessage());
        }
    }

    private static Map<String, Integer> flattenScores(Map<String, Map<String, Integer>> scores) {
        Map<String, Integer> flatScores = new HashMap<>();
        scores.forEach((org1, row) -> {
            row.forEach((org2, score) -> {
                if (!flatScores.containsKey(org2 + "_" + org1)) {
                    flatScores.put(org1 + "_" + org2, score);
                }
            });
        });
        return flatScores;
    }
}