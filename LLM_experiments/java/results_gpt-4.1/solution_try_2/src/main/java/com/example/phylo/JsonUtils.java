package com.example.phylo;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.File;
import java.io.IOException;
import java.util.Map;

public class JsonUtils {
    private static final ObjectMapper OBJECT_MAPPER = new ObjectMapper();

    public static Map<String, String> readOrganisms(String path) throws IOException {
        return OBJECT_MAPPER.readValue(new File(path), new TypeReference<>() {});
    }

    public static Map<String, Integer> readBlosum(String path) throws IOException {
        return OBJECT_MAPPER.readValue(new File(path), new TypeReference<>() {});
    }
}