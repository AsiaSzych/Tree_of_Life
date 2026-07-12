package com.example.phylo;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.File;
import java.io.IOException;
import java.util.Map;
import java.util.List;

public class JsonUtils {

  private static final ObjectMapper OBJECT_MAPPER = new ObjectMapper();

  public static Map<String, String> readOrganisms(String path) throws IOException {
    return OBJECT_MAPPER.readValue(
        new File(path), new TypeReference<Map<String, String>>() {});
  }

  public static Map<String, Integer> readBlosumMatrix(String path) throws IOException {
    return OBJECT_MAPPER.readValue(
        new File(path), new TypeReference<Map<String, Integer>>() {});
  }

  public static void writeScores(String path, Map<String, Integer> scores) throws IOException {
    OBJECT_MAPPER.writerWithDefaultPrettyPrinter().writeValue(new File(path), scores);
  }

  public static void writeClusters(String path, Map<Integer, List<List<String>>> clusters) throws IOException {
    OBJECT_MAPPER.writerWithDefaultPrettyPrinter().writeValue(new File(path), clusters);
  }
}