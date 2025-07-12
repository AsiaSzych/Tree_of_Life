package com.example.phylo;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

public class Main {

  public static void main(String[] args) throws IOException {
    if (args.length != 2) {
      System.err.println("Usage: java -jar phylo.jar organisms.json blosumXX.json");
      System.exit(1);
    }

    String organismsPath = args[0];
    String blosumPath = args[1];

    Map<String, String> organisms = JsonUtils.readOrganisms(organismsPath);
    Map<String, Integer> blosumMap = JsonUtils.readBlosumMatrix(blosumPath);

    BlosumMatrix blosumMatrix = new BlosumMatrix(blosumMap);
    NeedlemanWunsch nw = new NeedlemanWunsch(blosumMatrix);

    PairwiseScoreTable scoreTable = new PairwiseScoreTable();

    var speciesList = organisms.keySet().stream().toList();
    int n = speciesList.size();

    for (int i = 0; i < n; i++) {
      for (int j = i + 1; j < n; j++) {
        String speciesA = speciesList.get(i);
        String speciesB = speciesList.get(j);
        String seqA = organisms.get(speciesA);
        String seqB = organisms.get(speciesB);
        int score = nw.compute(seqA, seqB);
        scoreTable.put(speciesA, speciesB, score);
        System.out.printf("Score between '%s' and '%s': %d%n", speciesA, speciesB, score);
      }
    }

    // Save scores as before
    String blosumSuffix = blosumPath.toLowerCase().contains("blosum50") ? "blosum50"
        : blosumPath.toLowerCase().contains("blosum62") ? "blosum62" : "blosum";
    String outputFile = "organisms_scores_" + blosumSuffix + ".json";
    JsonUtils.writeScores(outputFile, scoreTable.toFlatMap());
    System.out.println("Pairwise scores saved to: " + outputFile);

    // Build the phylogenetic tree
    PhyloTreeBuilder treeBuilder = new PhyloTreeBuilder();
    PhyloNode root = treeBuilder.buildTree(scoreTable.toFlatMap(), organisms.keySet());
    System.out.println("Phylogenetic tree built. Root height (score): " + root.getHeight());

    // Export tree to Newick formats
    String newickFile = "tree_" + blosumSuffix + "_newick.nw";
    String newickWithDistFile = "tree_" + blosumSuffix + "_newick_with_distance.nw";

    String newick = NewickExporter.toNewick(root);
    String newickWithDist = NewickExporter.toNewickWithDistances(root);

    Files.writeString(Paths.get(newickFile), newick);
    Files.writeString(Paths.get(newickWithDistFile), newickWithDist);

    System.out.println("Tree saved in Newick format (leaves only): " + newickFile);
    System.out.println("Tree saved in Newick format (with distances): " + newickWithDistFile);

    // Draw dendrogram
    String dendrogramFile = "phylogenetic_tree_" + blosumSuffix + ".png";
    try {
      DendrogramDrawer.drawDendrogram(root, dendrogramFile);
      System.out.println("Dendrogram saved to: " + dendrogramFile);
    } catch (Exception e) {
      System.err.println("Failed to draw dendrogram: " + e.getMessage());
    }

    // --- CLUSTERING BASED ON THRESHOLDS ---
    // Read thresholds from file
    List<Integer> thresholds = new ArrayList<>();
    try {
      for (String line : Files.readAllLines(Paths.get("thresholds.txt"))) {
        line = line.trim();
        if (!line.isEmpty()) {
          thresholds.add(Integer.parseInt(line));
        }
      }
    } catch (IOException e) {
      System.err.println("Could not read thresholds.txt: " + e.getMessage());
      return;
    }

    // For each threshold, find clusters and print/save them
    Map<Integer, List<List<String>>> allClusters = new TreeMap<>();
    for (int threshold : thresholds) {
      List<List<String>> clusters = ClusterFinder.findClusters(root, threshold);
      allClusters.put(threshold, clusters);

      System.out.println("Clusters for threshold " + threshold + ":");
      for (List<String> cluster : clusters) {
        System.out.println("  " + cluster);
      }
    }

    // Save clusters to JSON
    String clustersFile = "clusters_for_" + blosumSuffix + ".json";
    JsonUtils.writeClusters(clustersFile, allClusters);
    System.out.println("Clusters saved to: " + clustersFile);
  }
}