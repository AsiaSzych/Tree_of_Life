package com.phylo.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.phylo.model.PhylogeneticNode;

import java.nio.file.Files;
import java.nio.file.Path;
import java.io.IOException;
import java.io.File;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class ThresholdClusterFinder {
    private static final ObjectMapper mapper = new ObjectMapper();

    public static Map<Integer, List<List<String>>> findClusters(PhylogeneticNode root, String thresholdsPath) 
            throws IOException {
        List<Integer> thresholds = readThresholds(thresholdsPath);
        Map<Integer, List<List<String>>> result = new HashMap<>();

        for (int threshold : thresholds) {
            List<List<String>> clusters = new ArrayList<>();
            findClustersRecursive(root,root, threshold, clusters);
            result.put(threshold, clusters);
        }

        return result;
    }

    private static List<Integer> readThresholds(String filePath) throws IOException {
        List<String> lines = Files.readAllLines(Path.of(filePath));
        return lines.stream()
                .map(String::trim)
                .filter(s -> !s.isEmpty())
                .map(Integer::parseInt)
                .toList();
    }

    private static void findClustersRecursive(PhylogeneticNode node, PhylogeneticNode root, int threshold, 
                                           List<List<String>> clusters) {
        if (node.getHeight() >= threshold || node == root) {
            List<String> cluster = new ArrayList<>();
            collectLeaves(node, cluster);
            if (!cluster.isEmpty()) {
                clusters.add(cluster);
            }
        } else {
            for (PhylogeneticNode child : node.getChildren()) {
                findClustersRecursive(child, root, threshold, clusters);
            }
        }
    }

    private static void collectLeaves(PhylogeneticNode node, List<String> leaves) {
        if (node.isLeaf()) {
            leaves.add(node.getName());
        } else {
            for (PhylogeneticNode child : node.getChildren()) {
                collectLeaves(child, leaves);
            }
        }
    }

    public static void saveClustersToFile(Map<Integer, List<List<String>>> clusters, 
                                        String blosumType) throws IOException {
        String filename = "./clusters_for_blosum" + blosumType + ".json";
        mapper.writerWithDefaultPrettyPrinter()
              .writeValue(new File(filename), clusters);
    }
}