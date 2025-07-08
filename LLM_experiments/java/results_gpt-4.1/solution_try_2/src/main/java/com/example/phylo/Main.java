package com.example.phylo;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class Main {

    public static void main(String[] args) {
        String organismsPath = "./organisms.json";
        String blosumPath = "./blosum62.json"; // Replace XX with 50 or 62 as needed
        String blosumType = null;
        PhyloNode root = null;
        try {
            Map<String, String> organisms = JsonUtils.readOrganisms(organismsPath);
            Map<String, Integer> blosumRaw = JsonUtils.readBlosum(blosumPath);

            BlosumMatrix blosumMatrix = new BlosumMatrix(blosumRaw);
            NeedlemanWunsch nw = new NeedlemanWunsch(blosumMatrix);
            SimilarityMatrix similarityMatrix = new SimilarityMatrix();

            List<String> speciesList = new ArrayList<>(organisms.keySet());
            int n = speciesList.size();

            for (int i = 0; i < n; i++) {
                for (int j = i + 1; j < n; j++) {
                    String s1 = speciesList.get(i);
                    String s2 = speciesList.get(j);
                    String seq1 = organisms.get(s1);
                    String seq2 = organisms.get(s2);
                    int score = nw.align(seq1, seq2);
                    similarityMatrix.put(s1, s2, score);
                    System.out.printf("Score between '%s' and '%s': %d%n", s1, s2, score);
                }
            }

            // Save similarity matrix
            blosumType = blosumPath.replaceAll("^.*blosum(\\d+)\\.json$", "$1");
            String outputFile = "./organisms_scores_blosum" + blosumType + ".json";
            similarityMatrix.saveToFile(outputFile);
            System.out.println("Similarity scores saved to: " + outputFile);

            // Build phylogenetic tree
            PhyloTreeBuilder treeBuilder = new PhyloTreeBuilder();
            root = treeBuilder.buildTree(similarityMatrix, speciesList);
            System.out.println("Phylogenetic tree built. Root node height: " + root.getHeight());

            // (Future: Save tree, draw dendrogram, export Newick, etc.)

        } catch (IOException e) {
            System.err.println("Error reading input files or saving output: " + e.getMessage());
            e.printStackTrace();
        }
        String treeSimpleFile = "./tree_blosum" + blosumType + "_newick.nw";
        String treeWithDistFile = "./tree_blosum" + blosumType + "_newick_with_distance.nw";
        try {
            NewickExporter.exportSimple(root, treeSimpleFile);
            System.out.println("Tree saved in Newick format (simple): " + treeSimpleFile);

            NewickExporter.exportWithDistances(root, treeWithDistFile);
            System.out.println("Tree saved in Newick format (with distances): " + treeWithDistFile);
        } catch (IOException e) {
            System.err.println("Error saving Newick files: " + e.getMessage());
        }
        String dendrogramFile = "./phylogenetic_tree_blosum" + blosumType + ".png";
        try {
            DendrogramDrawer.drawDendrogram(root, dendrogramFile);
            System.out.println("Dendrogram saved as: " + dendrogramFile);
        } catch (IOException e) {
            System.err.println("Error saving dendrogram PNG: " + e.getMessage());
        }

        String thresholdsFile = "./thresholds.txt";
        String clustersFile = "./clusters_for_blosum" + blosumType + ".json";
        try {
            List<Integer> thresholds = ThresholdUtils.readThresholds(thresholdsFile);

            // Map: threshold -> list of clusters (each cluster is a list of species)
            Map<Integer, List<List<String>>> allClusters = new java.util.LinkedHashMap<>();

            for (int threshold : thresholds) {
                List<List<String>> clusters = ClusterExtractor.extractClusters(root, threshold);
                allClusters.put(threshold, clusters);

                // Print clusters to standard output
                System.out.println("Threshold: " + threshold);
                int idx = 1;
                for (List<String> cluster : clusters) {
                    System.out.println("  Cluster " + idx + ": " + cluster);
                    idx++;
                }
            }

            // Save clusters to JSON file
            com.fasterxml.jackson.databind.ObjectMapper mapper = new com.fasterxml.jackson.databind.ObjectMapper();
            mapper.writerWithDefaultPrettyPrinter().writeValue(new java.io.File(clustersFile), allClusters);
            System.out.println("Clusters saved to: " + clustersFile);

        } catch (IOException e) {
            System.err.println("Error reading thresholds or saving clusters: " + e.getMessage());
        }
    }
}

