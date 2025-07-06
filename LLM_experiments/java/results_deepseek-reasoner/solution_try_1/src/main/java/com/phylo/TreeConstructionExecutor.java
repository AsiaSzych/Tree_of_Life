package com.phylo;

import com.phylo.model.PhyloNode;
import com.phylo.util.JsonReader;
import com.phylo.util.NewickFormatter;
import com.phylo.util.SimilarityMatrixLoader;
import com.phylo.util.DendrogramPlotter;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class TreeConstructionExecutor {
    public static void main(String[] args) {
        if (args.length < 2) {
            System.err.println("Usage: TreeConstructionExecutor <organisms_scores_blosumXX.json> <organisms.json>");
            System.exit(1);
        }

        try {
            // Extract BLOSUM type
            String blosumType = extractBlosumType(args[0]);
            
            // Load species and build tree
            Map<String, String> speciesMap = JsonReader.readMapFromJson(
                args[1], String.class, String.class
            );
            List<String> species = new ArrayList<>(speciesMap.keySet());
            Collections.sort(species);
            
            Map<String, Integer> pairwiseScores = JsonReader.readMapFromJson(
                args[0], String.class, Integer.class
            );
            Map<String, Map<String, Integer>> similarityMatrix = 
                SimilarityMatrixLoader.loadSimilarityMatrix(pairwiseScores, species);
            
            PhylogeneticTreeBuilder builder = new PhylogeneticTreeBuilder(similarityMatrix, species);
            PhyloNode root = builder.buildTree();
            
            // Generate Newick formats
            String newickWithoutDistances = NewickFormatter.toNewickWithoutDistances(root) + ";";
            String newickWithDistances = NewickFormatter.toNewickWithDistances(root, root.getHeight()) + ";";
            saveNewickFile("tree_blosum" + blosumType + "_newick.nw", newickWithoutDistances);
            saveNewickFile("tree_blosum" + blosumType + "_newick_with_distance.nw", newickWithDistances);
            
            // Generate dendrogram
            DendrogramPlotter.plotDendrogram(root, blosumType);
            
            // Threshold-based clustering
            List<Integer> thresholds = readThresholds();
            Map<Integer, List<List<String>>> thresholdClusters = new HashMap<>();
            
            for (int threshold : thresholds) {
                List<List<String>> clusters = ClusterFinder.findClusters(root, species, threshold);
                thresholdClusters.put(threshold, clusters);
                
                // Print to console
                System.out.println("\nThreshold: " + threshold);
                for (int i = 0; i < clusters.size(); i++) {
                    System.out.println("Cluster " + (i+1) + ": " + clusters.get(i));
                }
            }
            
            // Save clusters to JSON
            saveClusters(thresholdClusters, blosumType);
            
            System.out.println("All tasks completed successfully");
        } catch (IOException e) {
            System.err.println("Error: " + e.getMessage());
            System.exit(1);
        }
    }

    private static List<Integer> readThresholds() throws IOException {
        List<String> lines = Files.readAllLines(Paths.get("./thresholds.txt"));
        List<Integer> thresholds = new ArrayList<>();
        for (String line : lines) {
            thresholds.add(Integer.parseInt(line.trim()));
        }
        return thresholds;
    }

    private static void saveClusters(Map<Integer, List<List<String>>> clusters, String blosumType) 
            throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        String fileName = "clusters_for_blosum" + blosumType + ".json";
        mapper.writeValue(new File(fileName), clusters);
    }
    
    private static String extractBlosumType(String filePath) {
        File file = new File(filePath);
        String fileName = file.getName();
        // Extract "XX" from "organisms_scores_blosumXX.json"
        return fileName.replace("organisms_scores_blosum", "").replace(".json", "");
    }

    private static void saveNewickFile(String filename, String content) throws IOException {
        try (PrintWriter writer = new PrintWriter(Files.newBufferedWriter(Paths.get(filename)))) {
            writer.println(content);
        }
    }
}
