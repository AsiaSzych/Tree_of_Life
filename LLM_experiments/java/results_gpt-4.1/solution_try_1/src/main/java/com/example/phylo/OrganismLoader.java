package com.example.phylo;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.File;
import java.io.IOException;
import java.util.Map;

public class OrganismLoader {
  public static Map<String, String> loadOrganisms(String filePath) throws IOException {
    ObjectMapper mapper = new ObjectMapper();
    return mapper.readValue(new File(filePath), new TypeReference<Map<String, String>>() {});
  }
}