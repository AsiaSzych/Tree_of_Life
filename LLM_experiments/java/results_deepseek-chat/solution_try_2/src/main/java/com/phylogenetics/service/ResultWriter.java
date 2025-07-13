package com.phylogenetics.service;

import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.File;
import java.io.IOException;
import java.util.Map;

/**
 * Handles writing alignment results to JSON files.
 */
public class ResultWriter {
    private static final ObjectMapper objectMapper = new ObjectMapper();
    private static final String OUTPUT_PREFIX = "./organisms_scores_blosum";
    private static final String OUTPUT_SUFFIX = ".json";

    public static void writeResults(
            Map<String, Map<String, Integer>> scores,
            String blosumType) throws IOException {
        // Convert nested map to flat key-value pairs
        Map<String, Integer> flatScores = flattenScores(scores);
        String outputPath = OUTPUT_PREFIX + blosumType + OUTPUT_SUFFIX;
        objectMapper.writerWithDefaultPrettyPrinter()
                .writeValue(new File(outputPath), flatScores);
    }

    private static Map<String, Integer> flattenScores(
            Map<String, Map<String, Integer>> scores) {
        Map<String, Integer> flatScores = new java.util.HashMap<>();
        scores.forEach((org1, row) -> {
            row.forEach((org2, score) -> {
                // Only store each pair once (avoid duplicates)
                if (!flatScores.containsKey(org2 + "_" + org1)) {
                    flatScores.put(org1 + "_" + org2, score);
                }
            });
        });
        return flatScores;
    }
}