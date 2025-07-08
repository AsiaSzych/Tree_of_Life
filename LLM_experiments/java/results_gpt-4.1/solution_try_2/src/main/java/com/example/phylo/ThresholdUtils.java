package com.example.phylo;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class ThresholdUtils {

    /**
     * Reads integer thresholds from a file (one per line).
     */
    public static List<Integer> readThresholds(String filePath) throws IOException {
        List<Integer> thresholds = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            String line;
            while ((line = reader.readLine()) != null) {
                line = line.trim();
                if (!line.isEmpty()) {
                    thresholds.add(Integer.parseInt(line));
                }
            }
        }
        return thresholds;
    }
}