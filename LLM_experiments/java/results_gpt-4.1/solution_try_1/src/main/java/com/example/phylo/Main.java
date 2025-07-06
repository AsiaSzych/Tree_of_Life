package com.example.phylo;

import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.File;
import java.io.IOException;
import java.util.*;

public class Main {
  public static void main(String[] args) throws IOException {
    if (args.length != 2) {
      System.err.println("Usage: java -jar phylo.jar <organisms.json> <blosumXX.json>");
      System.exit(1);
    }

    String organismsPath = args[0];
    String blosumPath = args[1];

    Map<String, String> organisms = OrganismLoader.loadOrganisms(organismsPath);
    BlosumMatrix blosumMatrix = BlosumMatrixLoader.loadBlosumMatrix(blosumPath);

    List<String> species = organisms.keySet().stream().toList();
    SimilarityMatrix similarityMatrix = new SimilarityMatrix();

    for (int i = 0; i < species.size(); i++) {
      for (int j = i + 1; j < species.size(); j++) {
        String species1 = species.get(i);
        String species2 = species.get(j);
        String seq1 = organisms.get(species1);
        String seq2 = organisms.get(species2);

        int score = NeedlemanWunsch.align(seq1, seq2, blosumMatrix);
        similarityMatrix.put(species1, species2, score);
      }
    }

    // Save similarity matrix to file as before
    String blosumType = extractBlosumType(blosumPath);
    String outputFileName = "organisms_scores_blosum" + blosumType + ".json";
    similarityMatrix.saveToFile(outputFileName);
    System.out.println("Similarity scores saved to: " + outputFileName);

    // Build the phylogenetic tree
    PhyloNode root = PhyloTreeBuilder.buildTree(species, similarityMatrix);
    System.out.println("Phylogenetic tree built. Root node height: " + root.getHeight());

    // Export to Newick formats
    String newickFile = "tree_blosum" + blosumType + "_newick.nw";
    String newickWithDistFile = "tree_blosum" + blosumType + "_newick_with_distance.nw";
    NewickExporter.exportSimple(root, newickFile);
    NewickExporter.exportWithDistances(root, newickWithDistFile);
    System.out.println("Tree exported to Newick format: " + newickFile);
    System.out.println("Tree exported to Newick with distances: " + newickWithDistFile);

    // Draw dendrogram
    String dendrogramFile = "phylogenetic_tree_blosum" + blosumType + ".png";
    DendrogramDrawer.drawDendrogram(root, dendrogramFile);
    System.out.println("Dendrogram saved to: " + dendrogramFile);

    // --- CLUSTERING BY THRESHOLD ---
    String thresholdsFile = "thresholds.txt";
    List<Integer> thresholds = ThresholdLoader.loadThresholds(thresholdsFile);
    Map<Integer, List<List<String>>> clustersByThreshold = ThresholdClusterer.getClustersForThresholds(root, thresholds);

    // Print clusters to standard output
    for (int threshold : thresholds) {
      System.out.println("Threshold: " + threshold);
      List<List<String>> clusters = clustersByThreshold.get(threshold);
      for (int i = 0; i < clusters.size(); i++) {
        System.out.println("  Cluster " + (i + 1) + ": " + clusters.get(i));
      }
    }

    // Save clusters to JSON
    String clustersOutFile = "clusters_for_blosum" + blosumType + ".json";
    ObjectMapper mapper = new ObjectMapper();
    mapper.writerWithDefaultPrettyPrinter().writeValue(new File(clustersOutFile), clustersByThreshold);
    System.out.println("Clusters saved to: " + clustersOutFile);
  }

  private static String extractBlosumType(String blosumPath) {
    String fileName = blosumPath.substring(blosumPath.lastIndexOf('/') + 1);
    int start = fileName.indexOf("blosum") + 6;
    int end = fileName.indexOf('.', start);
    if (start > 5 && end > start) {
      return fileName.substring(start, end);
    }
    throw new IllegalArgumentException("Invalid BLOSUM filename: " + blosumPath);
  }
}
