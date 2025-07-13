package com.phylo.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.phylo.util.Pair;

import java.io.File;
import java.io.IOException;
import java.util.Map;

/**
 * Handles writing alignment scores to JSON files.
 */
public class ScoreWriter {
    private static final ObjectMapper mapper = new ObjectMapper();
    private static final String SCORE_FILE_PREFIX = "./organisms_scores_blosum";
    
    public static void writeScores(Map<Pair<String>, Integer> scores, String blosumType) 
        throws IOException {
        // Convert Pair keys to concatenated strings
        Map<String, Integer> outputMap = new java.util.HashMap<>();
        scores.forEach((pair, score) -> 
            outputMap.put(pair.first() + "_" + pair.second(), score));
        
        String outputPath = SCORE_FILE_PREFIX + blosumType + ".json";
        mapper.writerWithDefaultPrettyPrinter()
              .writeValue(new File(outputPath), outputMap);
    }
}