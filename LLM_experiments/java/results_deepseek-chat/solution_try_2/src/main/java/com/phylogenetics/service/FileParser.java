package com.phylogenetics.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.phylogenetics.model.Organism;
import com.phylogenetics.model.SubstitutionMatrix;

import java.io.File;
import java.io.IOException;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * Handles parsing of input JSON files.
 */
public class FileParser {
    private static final ObjectMapper objectMapper = new ObjectMapper();

    public static Map<String, Organism> parseOrganisms(String filePath) throws IOException {
        Map<String, String> rawMap = objectMapper.readValue(
            new File(filePath),
            new TypeReference<>() {}
        );
        
        return rawMap.entrySet().stream()
            .collect(Collectors.toMap(
                Map.Entry::getKey,
                entry -> new Organism(entry.getKey(), entry.getValue())
            ));
    }

    public static SubstitutionMatrix parseSubstitutionMatrix(String filePath) throws IOException {
        Map<String, Integer> matrix = objectMapper.readValue(
            new File(filePath),
            new TypeReference<>() {}
        );
        return new SubstitutionMatrix(matrix);
    }
}