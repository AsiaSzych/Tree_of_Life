package com.phylo.model;

import java.util.Map;

/**
 * Container for species and their amino acid sequences.
 */
public record Organisms(Map<String, String> speciesMap) {
    public String getSequence(String species) {
        return speciesMap.get(species);
    }
}