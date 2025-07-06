package com.example.phylo;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.File;
import java.io.IOException;
import java.util.Map;

public class BlosumMatrixLoader {
  public static BlosumMatrix loadBlosumMatrix(String filePath) throws IOException {
    ObjectMapper mapper = new ObjectMapper();
    Map<String, Integer> matrix = mapper.readValue(new File(filePath), new TypeReference<Map<String, Integer>>() {});
    return new BlosumMatrix(matrix);
  }
}
