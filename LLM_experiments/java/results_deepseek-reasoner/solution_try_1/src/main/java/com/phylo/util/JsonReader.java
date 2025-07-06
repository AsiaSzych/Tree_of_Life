package com.phylo.util;

import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Map;

public class JsonReader {
    private static final ObjectMapper objectMapper = new ObjectMapper();

    public static <K, V> Map<K, V> readMapFromJson(String filePath, Class<K> keyClass, Class<V> valueClass) 
            throws IOException {
        File file = new File(filePath);
        return objectMapper.readValue(file, 
            objectMapper.getTypeFactory().constructMapType(Map.class, keyClass, valueClass));
    }

    public static String readFileAsString(String filePath) throws IOException {
        return new String(Files.readAllBytes(Paths.get(filePath)));
    }
}