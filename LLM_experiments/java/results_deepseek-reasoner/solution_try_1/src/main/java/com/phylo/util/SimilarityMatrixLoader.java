package com.phylo.util;

import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.File;
import java.io.IOException;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class SimilarityMatrixLoader {
    private static final ObjectMapper mapper = new ObjectMapper();

    public static Map<String, Integer> loadPairwiseScores(String filePath) throws IOException {
        File file = new File(filePath);
        return mapper.readValue(file, 
            mapper.getTypeFactory().constructMapType(Map.class, String.class, Integer.class));
    }

    public static Map<String, Map<String, Integer>> loadSimilarityMatrix(
            Map<String, Integer> pairwiseScores, List<String> species) {
        
        Map<String, Map<String, Integer>> matrix = new HashMap<>();
        
        // Initialize matrix with species as keys
        for (String s : species) {
            matrix.put(s, new HashMap<>());
        }
        
        // Populate the matrix with pairwise scores
        for (Map.Entry<String, Integer> entry : pairwiseScores.entrySet()) {
            String[] parts = entry.getKey().split("_");
            if (parts.length != 2) continue;
            
            String species1 = parts[0];
            String species2 = parts[1];
            int score = entry.getValue();
            
            matrix.get(species1).put(species2, score);
            matrix.get(species2).put(species1, score);
        }
        
        return Collections.unmodifiableMap(matrix);
    }
}