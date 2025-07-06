package com.mycompany.phylogeny.io;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Utility class for saving analysis results to the file system.
 */
public final class ResultsSaver {

  private static final ObjectMapper OBJECT_MAPPER =
      new ObjectMapper().enable(SerializationFeature.INDENT_OUTPUT);

  private ResultsSaver() {
    // Private constructor to prevent instantiation
  }

  /**
   * Saves the calculated similarity scores to a JSON file.
   * The scores are flattened from a nested map to a single map with a "species1_species2" key.
   *
   * @param scores The nested map of similarity scores.
   * @param outputPath The path where the JSON file will be saved.
   * @throws IOException if an I/O error occurs during writing.
   */
  public static void saveScores(Map<String, Map<String, Integer>> scores, Path outputPath)
      throws IOException {
    Map<String, Integer> flatScores = flattenScores(scores);
    Files.createDirectories(outputPath.getParent());
    OBJECT_MAPPER.writeValue(outputPath.toFile(), flatScores);
  }

  /**
   * Saves a given string content to a text file.
   *
   * @param content The string content to write.
   * @param outputPath The path where the text file will be saved.
   * @throws IOException if an I/O error occurs during writing.
   */
  public static void saveTextFile(String content, Path outputPath) throws IOException {
    Files.createDirectories(outputPath.getParent());
    Files.writeString(outputPath, content);
  }

  /**
   * Saves the final cluster data to a JSON file.
   *
   * @param allClusters A map where the key is the threshold and the value is the list of clusters.
   * @param outputPath The path where the JSON file will be saved.
   * @throws IOException if an I/O error occurs during writing.
   */
  public static void saveClusters(
      Map<Integer, List<List<String>>> allClusters, Path outputPath) throws IOException {
    Files.createDirectories(outputPath.getParent());
    OBJECT_MAPPER.writeValue(outputPath.toFile(), allClusters);
  }

  private static Map<String, Integer> flattenScores(Map<String, Map<String, Integer>> scores) {
    Map<String, Integer> flatMap = new LinkedHashMap<>();
    scores.forEach(
        (species1, innerMap) ->
            innerMap.forEach(
                (species2, score) -> {
                  String key = species1 + "_" + species2;
                  flatMap.put(key, score);
                }));
    return flatMap;
  }
}