package com.phylo.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.phylo.model.BlosumMatrix;
import com.phylo.model.Organisms;
import java.io.File;
import java.io.IOException;
import java.util.Map;

/**
 * Handles reading JSON input files.
 */
public class FileService {
    private static final ObjectMapper mapper = new ObjectMapper();

    public static Organisms readOrganisms(String filePath) throws IOException {
        Map<String, String> speciesMap = mapper.readValue(
            new File(filePath), 
            new com.fasterxml.jackson.core.type.TypeReference<>() {}
        );
        return new Organisms(speciesMap);
    }

    public static BlosumMatrix readBlosumMatrix(String filePath, int defaultGapPenalty) throws IOException {
        Map<String, Integer> scoreMap = mapper.readValue(
            new File(filePath), 
            new com.fasterxml.jackson.core.type.TypeReference<>() {}
        );
        return new BlosumMatrix(scoreMap, defaultGapPenalty);
    }
    
    public static void saveScoresToFile(
        Map<String, Integer> scores, 
        String blosumType) throws IOException {
        String outputPath = "./organisms_scores_blosum" + blosumType + ".json";
        mapper.writeValue(new File(outputPath), scores);
    }
}