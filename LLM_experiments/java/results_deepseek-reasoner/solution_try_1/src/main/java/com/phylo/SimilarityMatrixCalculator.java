package com.phylo;

import com.phylo.util.JsonReader;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class SimilarityMatrixCalculator {
    public static void main(String[] args) {
        if (args.length < 2) {
            System.err.println("Usage: SimilarityMatrixCalculator <organisms.json> <blosumXX.json>");
            System.exit(1);
        }

        try {
            // Read input files
            Map<String, String> speciesToSequence = JsonReader.readMapFromJson(
                args[0], String.class, String.class
            );
            String blosumFilePath = args[1];
            Map<String, Integer> blosumMap = JsonReader.readMapFromJson(
                blosumFilePath, String.class, Integer.class
            );

            // Extract BLOSUM type from filename
            String blosumType = extractBlosumType(blosumFilePath);
            NeedlemanWunschScorer scorer = new NeedlemanWunschScorer(blosumMap);
            List<String> speciesList = new ArrayList<>(speciesToSequence.keySet());
            Collections.sort(speciesList); // Sort for consistent ordering
            int n = speciesList.size();
            int[][] similarityMatrix = new int[n][n];
            
            // Create map for pairwise scores
            Map<String, Integer> pairwiseScores = new HashMap<>();

            // Compute pairwise scores
            for (int i = 0; i < n; i++) {
                String species1 = speciesList.get(i);
                String seq1 = speciesToSequence.get(species1);
                for (int j = i; j < n; j++) {
                    String species2 = speciesList.get(j);
                    String seq2 = speciesToSequence.get(species2);
                    int score = scorer.computeScore(seq1, seq2);
                    
                    // Store in matrix
                    similarityMatrix[i][j] = score;
                    similarityMatrix[j][i] = score;
                    
                    // Store in pairwise map (canonical key)
                    String pairKey = createCanonicalPairKey(species1, species2);
                    pairwiseScores.put(pairKey, score);
                }
            }

            // Save results
            saveSimilarityMatrix(speciesList, similarityMatrix);
            savePairwiseScores(pairwiseScores, blosumType);
            System.out.println("Output files generated successfully.");
        } catch (IOException e) {
            System.err.println("Error reading files: " + e.getMessage());
            System.exit(1);
        } catch (IllegalArgumentException e) {
            System.err.println("Validation error: " + e.getMessage());
            System.exit(1);
        }
    }

    private static String extractBlosumType(String filePath) {
        File file = new File(filePath);
        String fileName = file.getName();
        // Extract "XX" from "blosumXX.json"
        return fileName.replace("blosum", "").replace(".json", "");
    }

    private static String createCanonicalPairKey(String species1, String species2) {
        // Ensure consistent alphabetical ordering
        return species1.compareTo(species2) < 0 
            ? species1 + "_" + species2 
            : species2 + "_" + species1;
    }

    private static void saveSimilarityMatrix(List<String> species, int[][] matrix) 
            throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        File outputFile = new File("./similarity_matrix.json");
        mapper.writeValue(outputFile, Map.of(
            "species", species,
            "matrix", matrix
        ));
    }

    private static void savePairwiseScores(Map<String, Integer> scores, String blosumType) 
            throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        String fileName = "./organisms_scores_blosum" + blosumType + ".json";
        mapper.writeValue(new File(fileName), scores);
    }
}