package com.phylogen.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.phylogen.model.ScoringMatrix;
import com.phylogen.model.Species;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * Handles loading data from files into our application's models.
 */
public class DataLoader {

    private static final ObjectMapper objectMapper = new ObjectMapper();

    /**
     * Loads species data from a JSON file.
     *
     * @param path Path to the organisms.json file.
     * @return A list of Species objects.
     * @throws IOException if there is an error reading the file.
     */
    public List<Species> loadSpecies(Path path) throws IOException {
        Map<String, String> speciesMap = objectMapper.readValue(path.toFile(), new TypeReference<>() {});
        return speciesMap.entrySet().stream()
                .map(entry -> new Species(entry.getKey(), entry.getValue()))
                .collect(Collectors.toList());
    }

    /**
     * Loads the scoring matrix from a BLOSUM JSON file.
     *
     * @param path Path to the blosumXX.json file.
     * @return A ScoringMatrix object.
     * @throws IOException if there is an error reading the file.
     */
    public ScoringMatrix loadScoringMatrix(Path path) throws IOException {
        Map<String, Integer> rawScores = objectMapper.readValue(path.toFile(), new TypeReference<>() {});
        return new ScoringMatrix(rawScores);
    }

    /**
     * Loads clustering thresholds from a text file.
     * Each line in the file is expected to contain one integer threshold.
     *
     * @param path Path to the thresholds.txt file.
     * @return A list of integer thresholds.
     * @throws IOException if there is an error reading the file.
     */
    public List<Integer> loadThresholds(Path path) throws IOException {
        return Files.readAllLines(path).stream()
                .map(String::trim)
                .filter(line -> !line.isEmpty())
                .map(Integer::parseInt)
                .collect(Collectors.toList());
    }
}