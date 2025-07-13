package com.phylo;

import com.phylo.model.OrganismData;
import com.phylo.model.PhylogeneticNode;
import com.phylo.service.AlignmentService;
import com.phylo.service.DataLoader;
import com.phylo.service.NewickExporter;
import com.phylo.service.PhylogeneticTreeBuilder;
import com.phylo.service.ScoreWriter;
import com.phylo.service.DendrogramVisualizer;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import com.phylo.service.ThresholdClusterFinder;

import java.util.List;
import java.util.Map;

public class App {
    public static void main(String[] args) {
        if (args.length < 2) {
            System.err.println("Usage: java App <organisms.json> <blosumXX.json>");
            System.exit(1);
        }

        try {
            // Load data
            OrganismData organisms = DataLoader.loadOrganisms(args[0]);
            Path blosumPath = Paths.get(args[1]);
            String blosumType = extractBlosumType(blosumPath.getFileName().toString());
            
            // Calculate alignment scores
            AlignmentService alignmentService = new AlignmentService(DataLoader.loadBlosumMatrix(args[1]));
            var results = alignmentService.calculateAllPairs(organisms);
            
            // Save and print results
            ScoreWriter.writeScores(results, blosumType);
            results.forEach((pair, score) -> 
                System.out.printf("%s vs %s: %d%n", pair.first(), pair.second(), score));
            
            // Build phylogenetic tree
            PhylogeneticTreeBuilder treeBuilder = new PhylogeneticTreeBuilder(results);
            PhylogeneticNode root = treeBuilder.buildTree(organisms.speciesToSequence().keySet());
            
            // Generate both Newick formats
            String basicNewick = NewickExporter.toBasicNewick(root) + ";";
            String distanceNewick = NewickExporter.toDistanceNewick(root) + ";";
            
            // Save to files
            saveNewickFile("tree_blosum" + blosumType + "_newick.nw", basicNewick);
            saveNewickFile("tree_blosum" + blosumType + "_newick_with_distance.nw", distanceNewick);
            
            System.out.println("Basic Newick format saved to: tree_blosum" + blosumType + "_newick.nw");
            System.out.println("Distance Newick format saved to: tree_blosum" + blosumType + "_newick_with_distance.nw");
            
            try {
                DendrogramVisualizer.visualize(root, blosumType);
                System.out.println("Dendrogram saved to: phylogenetic_tree_blosum" + blosumType + ".png");
            } catch (IOException e) {
                System.err.println("Error generating dendrogram: " + e.getMessage());
            }    
            
            // Process thresholds
            Map<Integer, List<List<String>>> clusters = 
                ThresholdClusterFinder.findClusters(root, args[2]);
            
            // Print to console
            System.out.println("Clusters by threshold:");
            clusters.forEach((threshold, clusterList) -> {
                System.out.println("\nThreshold: " + threshold);
                clusterList.forEach(cluster -> 
                    System.out.println(" - " + String.join(", ", cluster)));
            });
            
            // Save to JSON
            ThresholdClusterFinder.saveClustersToFile(clusters, blosumType);
            System.out.println("\nClusters saved to: clusters_for_blosum" + blosumType + ".json");
            

        } catch (IOException e) {
            System.err.println("Error processing data: " + e.getMessage());
            System.exit(1);
        }
    }

    private static void saveNewickFile(String filename, String content) throws IOException {
        Files.writeString(Path.of("./" + filename), content);
    }

    private static String extractBlosumType(String filename) {
        return filename.replace("blosum", "").replace(".json", "");
    }
}