package com.phylo.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.phylo.model.BlosumMatrix;
import com.phylo.model.OrganismData;

import java.io.File;
import java.io.IOException;
import java.util.Map;

/**
 * Handles loading JSON data files.
 */
public class DataLoader {
    private static final ObjectMapper mapper = new ObjectMapper();

    public static OrganismData loadOrganisms(String filePath) throws IOException {
        Map<String, String> data = mapper.readValue(new File(filePath), 
            new TypeReference<>() {});
        OrganismData organismData = new OrganismData(data);
        organismData.validate();
        return organismData;
    }

    public static BlosumMatrix loadBlosumMatrix(String filePath) throws IOException {
        Map<String, Integer> data = mapper.readValue(new File(filePath), 
            new TypeReference<>() {});
        BlosumMatrix matrix = new BlosumMatrix(data);
        matrix.validate();
        return matrix;
    }
}