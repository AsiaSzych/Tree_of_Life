package com.mycompany.phylogeny;

import com.mycompany.phylogeny.algorithm.ClusterFinder;
import com.mycompany.phylogeny.algorithm.ClusteringResult;
import com.mycompany.phylogeny.algorithm.HierarchicalClusterer;
import com.mycompany.phylogeny.algorithm.NeedlemanWunschAligner;
import com.mycompany.phylogeny.domain.ScoringMatrix;
import com.mycompany.phylogeny.domain.Species;
import com.mycompany.phylogeny.domain.tree.TreeNode;
import com.mycompany.phylogeny.io.NewickTreeFormatter;
import com.mycompany.phylogeny.io.ResultsSaver;
import com.mycompany.phylogeny.loader.DataLoader;
import com.mycompany.phylogeny.visualization.DendrogramVisualizer;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class Main {

  // --- Configuration ---
  private static final Path ORGANISMS_FILE_PATH = Paths.get("data", "organisms.json");
  private static final Path BLOSUM_FILE_PATH = Paths.get("data", "blosum62.json");
  private static final Path THRESHOLDS_FILE_PATH = Paths.get("data", "thresholds.txt");
  // --- End Configuration ---

  public static void main(String[] args) {
    System.out.println("--- Starting Phylogenetic Analysis ---");

    try {
      // 1. Load data
      ScoringMatrix scoringMatrix = DataLoader.loadScoringMatrix(BLOSUM_FILE_PATH);
      List<Species> speciesList = DataLoader.loadSpecies(ORGANISMS_FILE_PATH);

      // 2. Calculate pairwise similarity scores
      NeedlemanWunschAligner aligner = new NeedlemanWunschAligner(scoringMatrix);
      Map<String, Map<String, Integer>> similarityScores =
          calculateAllPairsScores(speciesList, aligner);

      // 3. Build the phylogenetic tree
      HierarchicalClusterer clusterer = new HierarchicalClusterer();
      ClusteringResult clusteringResult = clusterer.buildTree(speciesList, similarityScores);
      System.out.println("\nPhylogenetic tree built successfully.");

      // 4. Generate and save all intermediate and visual results
      generateIntermediateOutputs(clusteringResult, speciesList, BLOSUM_FILE_PATH);

      // 5. Find and save clusters based on thresholds
      findAndSaveClusters(clusteringResult.rootNode(), BLOSUM_FILE_PATH);

      System.out.println("\n--- Analysis Complete ---");

    } catch (IOException e) {
      System.err.println("Error processing files: " + e.getMessage());
      e.printStackTrace();
    } catch (Exception e) {
      System.err.println("An unexpected error occurred: " + e.getMessage());
      e.printStackTrace();
    }
  }

  private static void findAndSaveClusters(TreeNode rootNode, Path blosumInputPath)
      throws IOException {
    System.out.println("\n--- Finding Clusters for Thresholds ---");
    List<Integer> thresholds = DataLoader.loadThresholds(THRESHOLDS_FILE_PATH);
    System.out.println("Loaded thresholds: " + thresholds);

    ClusterFinder clusterFinder = new ClusterFinder(rootNode);
    Map<Integer, List<List<String>>> allClusters = new LinkedHashMap<>();

    for (int threshold : thresholds) {
      List<List<String>> clusters = clusterFinder.findClusters(threshold);
      allClusters.put(threshold, clusters);

      System.out.printf("%n--- Clusters for threshold: %d ---%n", threshold);
      for (int i = 0; i < clusters.size(); i++) {
        System.out.printf("Cluster %d: %s%n", i + 1, clusters.get(i));
      }
    }

    Path clustersOutputPath = generateClustersOutputPath(blosumInputPath);
    ResultsSaver.saveClusters(allClusters, clustersOutputPath);
    System.out.printf("%nCluster results saved to: %s%n", clustersOutputPath);
  }

  private static void generateIntermediateOutputs(
      ClusteringResult clusteringResult, List<Species> speciesList, Path blosumInputPath)
      throws IOException {
    // Save Newick files
    saveNewickFiles(clusteringResult.rootNode(), blosumInputPath);

    // Save Dendrogram
    System.out.println("\n--- Generating Dendrogram ---");
    DendrogramVisualizer visualizer = new DendrogramVisualizer();
    List<String> speciesNames = speciesList.stream().map(Species::name).toList();
    Path dendrogramPath = generateDendrogramOutputPath(blosumInputPath);
    visualizer.saveDendrogram(clusteringResult, speciesNames, dendrogramPath);
    System.out.println("Dendrogram saved to: " + dendrogramPath);
  }

  private static void saveNewickFiles(TreeNode rootNode, Path blosumInputPath) throws IOException {
    System.out.println("\n--- Saving Tree in Newick Format ---");
    NewickTreeFormatter formatter = new NewickTreeFormatter();
    String simpleNewick = formatter.formatSimple(rootNode);
    Path simpleNewickPath = generateNewickOutputFilePath(blosumInputPath, false);
    ResultsSaver.saveTextFile(simpleNewick, simpleNewickPath);
    System.out.println("Saved simple Newick tree to: " + simpleNewickPath);
    String newickWithDistances = formatter.formatWithDistances(rootNode);
    Path newickWithDistancesPath = generateNewickOutputFilePath(blosumInputPath, true);
    ResultsSaver.saveTextFile(newickWithDistances, newickWithDistancesPath);
    System.out.println("Saved Newick tree with distances to: " + newickWithDistancesPath);
  }

  private static Map<String, Map<String, Integer>> calculateAllPairsScores(
      List<Species> speciesList, NeedlemanWunschAligner aligner) {
    System.out.println("\nCalculating pairwise scores...");
    Map<String, Map<String, Integer>> scores = new HashMap<>();
    for (int i = 0; i < speciesList.size(); i++) {
      for (int j = i + 1; j < speciesList.size(); j++) {
        Species s1 = speciesList.get(i);
        Species s2 = speciesList.get(j);
        int score = aligner.calculateScore(s1.sequence(), s2.sequence());
        String key1 = s1.name().compareTo(s2.name()) < 0 ? s1.name() : s2.name();
        String key2 = s1.name().compareTo(s2.name()) < 0 ? s2.name() : s1.name();
        scores.computeIfAbsent(key1, k -> new HashMap<>()).put(key2, score);
      }
    }
    return scores;
  }

  private static Path generateNewickOutputFilePath(Path blosumInputPath, boolean withDistance) {
    String baseName = getBlosumBaseName(blosumInputPath);
    String suffix = withDistance ? "_newick_with_distance.nw" : "_newick.nw";
    String outputFileName = String.format("tree_%s%s", baseName, suffix);
    return Paths.get("output", outputFileName);
  }

  private static Path generateDendrogramOutputPath(Path blosumInputPath) {
    String baseName = getBlosumBaseName(blosumInputPath);
    String outputFileName = String.format("phylogenetic_tree_%s.png", baseName);
    return Paths.get("output", outputFileName);
  }

  private static Path generateClustersOutputPath(Path blosumInputPath) {
    String baseName = getBlosumBaseName(blosumInputPath);
    String outputFileName = String.format("clusters_for_%s.json", baseName);
    return Paths.get("output", outputFileName);
  }

  private static String getBlosumBaseName(Path blosumInputPath) {
    String inputFileName = blosumInputPath.getFileName().toString();
    return inputFileName.substring(0, inputFileName.lastIndexOf('.'));
  }
}