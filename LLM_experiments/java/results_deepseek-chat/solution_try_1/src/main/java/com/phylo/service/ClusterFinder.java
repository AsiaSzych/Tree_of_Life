package com.phylo.service;

import com.phylo.model.ClusterNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.File;
import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;

/**
 * Handles threshold-based clustering from phylogenetic tree
 */
public class ClusterFinder {
    private static final ObjectMapper mapper = new ObjectMapper();

    public static Map<Integer, List<List<String>>> findClustersForThresholds(
            ClusterNode root, 
            String thresholdsFile,
            String blosumType) throws IOException {
        
        // Read thresholds
        List<Integer> thresholds = readThresholds(thresholdsFile);
        Map<Integer, List<List<String>>> result = new TreeMap<>(Collections.reverseOrder());

        // Find clusters for each threshold
        for (int threshold : thresholds) {
            List<List<String>> clusters = new ArrayList<>();
            findClusters(root, threshold, clusters);
            result.put(threshold, clusters);
        }

        // Save to JSON
        saveClustersToFile(result, blosumType);
        return result;
    }

    private static List<Integer> readThresholds(String filePath) throws IOException {
        return mapper.readValue(
            new File(filePath),
            new com.fasterxml.jackson.core.type.TypeReference<List<Integer>>() {}
        );
    }

    private static void findClusters(ClusterNode node, int threshold, List<List<String>> clusters) {
        if (node == null) return;

        if (node.isLeaf()) {
            clusters.add(Collections.singletonList(node.getLabel()));
        } else if (node.getHeight() > threshold) {
            // Node above threshold - continue searching children
            findClusters(node.getLeft(), threshold, clusters);
            findClusters(node.getRight(), threshold, clusters);
        } else {
            // Node below threshold - all descendants form one cluster
            List<String> cluster = new ArrayList<>();
            collectLeaves(node, cluster);
            clusters.add(cluster);
        }
    }

    private static void collectLeaves(ClusterNode node, List<String> leaves) {
        if (node.isLeaf()) {
            leaves.add(node.getLabel());
        } else {
            collectLeaves(node.getLeft(), leaves);
            collectLeaves(node.getRight(), leaves);
        }
    }

    private static void saveClustersToFile(
            Map<Integer, List<List<String>>> clusters, 
            String blosumType) throws IOException {
        
        String outputPath = "./clusters_for_blosum" + blosumType + ".json";
        mapper.writeValue(new File(outputPath), clusters);
    }
}