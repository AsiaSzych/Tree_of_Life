package com.phylogen.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Handles saving the calculated results to the file system.
 */
public class ResultsSaver {

    private final ObjectMapper objectMapper;

    public ResultsSaver() {
        this.objectMapper = new ObjectMapper();
        // Configure for pretty-printing the JSON output
        this.objectMapper.enable(SerializationFeature.INDENT_OUTPUT);
    }

    /**
     * Saves the pairwise similarity scores to a JSON file.
     *
     * @param scores     The nested map of scores (e.g., scores.get("SpeciesA").get("SpeciesB")).
     * @param outputPath The path where the JSON file will be saved.
     * @throws IOException if there is an error creating directories or writing the file.
     */
    public void saveScoresToJson(Map<String, Map<String, Integer>> scores, Path outputPath) throws IOException {
        // Ensure the parent directory exists
        if (outputPath.getParent() != null) {
            Files.createDirectories(outputPath.getParent());
        }

        // Flatten the nested map into the desired key-value format
        Map<String, Integer> flatScores = new HashMap<>();
        scores.forEach((species1, innerMap) -> {
            innerMap.forEach((species2, score) -> {
                // Create a sorted key to ensure consistency (e.g., "Horse_Wild boar" not "Wild boar_Horse")
                String key = species1.compareTo(species2) < 0
                        ? species1 + "_" + species2
                        : species2 + "_" + species1;
                flatScores.putIfAbsent(key, score);
            });
        });

        // Write the flattened map to the specified file
        objectMapper.writeValue(outputPath.toFile(), flatScores);
    }

    /**
     * Saves the extracted clusters for multiple thresholds to a JSON file.
     *
     * @param allClusters A map where the key is the threshold and the value is the list of clusters.
     * @param outputPath  The path where the JSON file will be saved.
     * @throws IOException if there is an error creating directories or writing the file.
     */
    public void saveClustersToJson(Map<Integer, List<List<String>>> allClusters, Path outputPath) throws IOException {
        if (outputPath.getParent() != null) {
            Files.createDirectories(outputPath.getParent());
        }
        objectMapper.writeValue(outputPath.toFile(), allClusters);
    }
}