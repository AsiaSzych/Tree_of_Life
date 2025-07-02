package com.phylogen;

import com.phylogen.model.ScoringMatrix;
import com.phylogen.model.Species;
import com.phylogen.model.TreeNode;
import com.phylogen.service.*;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class PhylogeneticAnalysisApp {

    public static void main(String[] args) {
        System.out.println("--- Running Main Project Logic ---");

        try {
            // --- Configuration ---
            Path speciesPath = Paths.get("data/input/organisms.json");
            Path blosumPath = Paths.get("data/input/blosum50.json");
            Path thresholdsPath = Paths.get("data/input/thresholds.txt");

            // --- 1. Load Data ---
            DataLoader loader = new DataLoader();
            List<Species> speciesList = loader.loadSpecies(speciesPath);
            ScoringMatrix scoringMatrix = loader.loadScoringMatrix(blosumPath);
            List<Integer> thresholds = loader.loadThresholds(thresholdsPath);
            System.out.println("Loaded " + speciesList.size() + " species and " + thresholds.size() + " thresholds.");
            System.out.println("Using scoring matrix from: " + blosumPath);

            // --- 2. Calculate Pairwise Scores ---
            NeedlemanWunschAligner aligner = new NeedlemanWunschAligner(scoringMatrix);
            Map<String, Map<String, Integer>> similarityScores = calculateAllScores(speciesList, aligner);

            // --- 3. Save Intermediate Scores ---
            ResultsSaver saver = new ResultsSaver();
            Path scoresOutputPath = generateScoresOutputFilePath(blosumPath);
            saver.saveScoresToJson(similarityScores, scoresOutputPath);
            System.out.println("Scores successfully saved to: " + scoresOutputPath);

            // --- 4. Build Phylogenetic Tree ---
            System.out.println("\nBuilding phylogenetic tree...");
            HierarchicalClusteringService clusteringService = new HierarchicalClusteringService(speciesList, similarityScores);
            TreeNode root = clusteringService.buildTree();
            System.out.println("Phylogenetic tree built successfully.");

            // --- 5. Export Tree to Newick Format ---
            System.out.println("\nExporting tree to Newick format...");
            NewickTreeExporter exporter = new NewickTreeExporter();
            Path simpleNewickPath = generateNewickOutputFilePath(blosumPath, false);
            saveStringToFile(exporter.toSimpleNewick(root), simpleNewickPath);
            System.out.println("Simple Newick tree saved to: " + simpleNewickPath);
            Path distanceNewickPath = generateNewickOutputFilePath(blosumPath, true);
            saveStringToFile(exporter.toNewickWithDistances(root, similarityScores), distanceNewickPath);
            System.out.println("Newick tree with distances saved to: " + distanceNewickPath);

            // --- 6. Draw and Save Dendrogram ---
            System.out.println("\nGenerating dendrogram...");
            DendrogramDrawer drawer = new DendrogramDrawer();
            Path dendrogramPath = generateDendrogramOutputFilePath(blosumPath);
            drawer.drawAndSave(root, dendrogramPath);
            System.out.println("Dendrogram saved to: " + dendrogramPath);

            // --- 7. Extract and Save Clusters by Threshold ---
            System.out.println("\n--- Final Cluster Analysis ---");
            ClusterExtractorService extractor = new ClusterExtractorService();
            Map<Integer, List<List<String>>> allClusters = new LinkedHashMap<>();
            for (int threshold : thresholds) {
                List<List<String>> clusters = extractor.findClustersForThreshold(root, threshold);
                allClusters.put(threshold, clusters);
                System.out.printf("\nClusters for threshold %d:\n", threshold);
                clusters.forEach(System.out::println);
            }
            Path clustersOutputPath = generateClustersOutputFilePath(blosumPath);
            saver.saveClustersToJson(allClusters, clustersOutputPath);
            System.out.println("\nCluster data saved to: " + clustersOutputPath);

        } catch (IOException e) {
            System.err.println("An error occurred during processing: " + e.getMessage());
            e.printStackTrace();
        }
    }

    private static Map<String, Map<String, Integer>> calculateAllScores(List<Species> speciesList, NeedlemanWunschAligner aligner) {
        Map<String, Map<String, Integer>> scores = new HashMap<>();
        System.out.println("\nCalculating pairwise similarity scores...");
        for (int i = 0; i < speciesList.size(); i++) {
            for (int j = i + 1; j < speciesList.size(); j++) {
                Species s1 = speciesList.get(i);
                Species s2 = speciesList.get(j);
                int score = aligner.calculateScore(s1.sequence(), s2.sequence());
                scores.computeIfAbsent(s1.name(), k -> new HashMap<>()).put(s2.name(), score);
                scores.computeIfAbsent(s2.name(), k -> new HashMap<>()).put(s1.name(), score);
            }
        }
        return scores;
    }

    private static Path generateScoresOutputFilePath(Path blosumPath) {
        String baseName = getBlosumBaseName(blosumPath);
        return Paths.get("data/output/", String.format("organisms_scores_%s.json", baseName));
    }

    private static Path generateNewickOutputFilePath(Path blosumPath, boolean withDistance) {
        String baseName = getBlosumBaseName(blosumPath);
        String suffix = withDistance ? "_newick_with_distance.nw" : "_newick.nw";
        return Paths.get("data/output/", String.format("tree_%s%s", baseName, suffix));
    }

    private static Path generateDendrogramOutputFilePath(Path blosumPath) {
        String baseName = getBlosumBaseName(blosumPath);
        return Paths.get("data/output/", String.format("phylogenetic_tree_%s.png", baseName));
    }

    private static Path generateClustersOutputFilePath(Path blosumPath) {
        String baseName = getBlosumBaseName(blosumPath);
        return Paths.get("data/output/", String.format("clusters_for_%s.json", baseName));
    }

    private static String getBlosumBaseName(Path blosumPath) {
        String fileName = blosumPath.getFileName().toString();
        return fileName.substring(0, fileName.lastIndexOf('.'));
    }

    private static void saveStringToFile(String content, Path path) throws IOException {
        if (path.getParent() != null) {
            Files.createDirectories(path.getParent());
        }
        Files.writeString(path, content);
    }
}