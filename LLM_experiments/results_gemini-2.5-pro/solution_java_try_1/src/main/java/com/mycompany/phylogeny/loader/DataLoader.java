package com.mycompany.phylogeny.loader;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.mycompany.phylogeny.domain.ScoringMatrix;
import com.mycompany.phylogeny.domain.Species;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * Utility class for loading data from files.
 */
public final class DataLoader {

  private static final ObjectMapper OBJECT_MAPPER = new ObjectMapper();

  private DataLoader() {
    // Private constructor to prevent instantiation
  }

  public static List<Species> loadSpecies(Path path) throws IOException {
    Map<String, String> speciesMap =
        OBJECT_MAPPER.readValue(path.toFile(), new TypeReference<>() {});
    return speciesMap.entrySet().stream()
        .map(entry -> new Species(entry.getKey(), entry.getValue()))
        .collect(Collectors.toList());
  }

  public static ScoringMatrix loadScoringMatrix(Path path) throws IOException {
    Map<String, Integer> scores =
        OBJECT_MAPPER.readValue(path.toFile(), new TypeReference<>() {});
    return new ScoringMatrix(scores);
  }

  /**
   * Loads a list of integer thresholds from a text file.
   * Each line in the file should contain a single integer.
   *
   * @param path The path to the thresholds text file.
   * @return A list of integer thresholds.
   * @throws IOException if an I/O error occurs.
   * @throws NumberFormatException if a line contains non-integer data.
   */
  public static List<Integer> loadThresholds(Path path) throws IOException {
    return Files.readAllLines(path).stream()
        .filter(line -> !line.isBlank())
        .map(Integer::parseInt)
        .collect(Collectors.toList());
  }
}