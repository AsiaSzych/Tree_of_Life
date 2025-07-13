package com.phylogenetics.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.phylogenetics.model.TreeNode;

import java.io.File;
import java.io.IOException;
import java.util.*;

/**
 * Finds clusters in phylogenetic tree based on similarity thresholds.
 */
public class ClusterFinder {
    private static final ObjectMapper objectMapper = new ObjectMapper();
    private static final String CLUSTER_PREFIX = "./clusters_for_blosum";
    private static final String CLUSTER_SUFFIX = ".json";

    public static void findAndSaveClusters(TreeNode root, String blosumType) throws IOException {
        // Read thresholds from file
        List<Integer> thresholds = readThresholds("./thresholds.txt");
        
        // Calculate clusters for each threshold
        Map<Integer, List<List<String>>> thresholdClusters = new TreeMap<>(Collections.reverseOrder());
        for (int threshold : thresholds) {
            List<List<String>> clusters = findClusters(root, threshold);
            thresholdClusters.put(threshold, clusters);
        }

        // Print to console
        printClusters(thresholdClusters);

        // Save to JSON
        String outputPath = CLUSTER_PREFIX + blosumType + CLUSTER_SUFFIX;
        objectMapper.writerWithDefaultPrettyPrinter()
                .writeValue(new File(outputPath), thresholdClusters);
    }

    private static List<Integer> readThresholds(String filePath) throws IOException {
        List<Integer> thresholds = new ArrayList<>();
        try (Scanner scanner = new Scanner(new File(filePath))) {
            while (scanner.hasNextInt()) {
                thresholds.add(scanner.nextInt());
            }
        }
        return thresholds;
    }

    private static List<List<String>> findClusters(TreeNode node, int threshold) {
        List<List<String>> clusters = new ArrayList<>();
        findClustersRecursive(node, threshold, clusters);
        return clusters;
    }

    private static void findClustersRecursive(TreeNode node, int threshold, List<List<String>> clusters) {
        if (node.getHeight() <= threshold) {
            // Below threshold - treat as separate clusters for each child
            for (TreeNode child : node.getChildren()) {
                findClustersRecursive(child, threshold, clusters);
            }
        } else {
            // Above threshold - collect all leaves under this node as one cluster
            List<String> cluster = new ArrayList<>();
            collectLeaves(node, cluster);
            if (!cluster.isEmpty()) {
                clusters.add(cluster);
            }
        }
    }

    private static void collectLeaves(TreeNode node, List<String> leaves) {
        if (node.isLeaf()) {
            leaves.add(node.getName());
        } else {
            for (TreeNode child : node.getChildren()) {
                collectLeaves(child, leaves);
            }
        }
    }

    private static void printClusters(Map<Integer, List<List<String>>> thresholdClusters) {
        System.out.println("Cluster Results:");
        for (Map.Entry<Integer, List<List<String>>> entry : thresholdClusters.entrySet()) {
            System.out.println("Threshold: " + entry.getKey());
            for (List<String> cluster : entry.getValue()) {
                System.out.println("\tCluster: " + cluster);
            }
        }
    }
}