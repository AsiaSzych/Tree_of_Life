package com.example.phylo;

import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class SimilarityMatrix {
    private final Map<Pair<String, String>, Integer> matrix = new HashMap<>();

    public void put(String species1, String species2, int score) {
        matrix.put(new Pair<>(species1, species2), score);
    }

    public int get(String species1, String species2) {
        return matrix.getOrDefault(new Pair<>(species1, species2), Integer.MIN_VALUE);
    }

    public Map<Pair<String, String>, Integer> getAll() {
        return matrix;
    }

    public void saveToFile(String filePath) throws IOException {
        Map<String, Integer> exportMap = new HashMap<>();
        for (Map.Entry<Pair<String, String>, Integer> entry : matrix.entrySet()) {
            String key = entry.getKey().getFirst() + "_" + entry.getKey().getSecond();
            exportMap.put(key, entry.getValue());
        }
        ObjectMapper mapper = new ObjectMapper();
        mapper.writerWithDefaultPrettyPrinter().writeValue(new File(filePath), exportMap);
    }
}