package com.phylo.model;

import java.util.Map;

/**
 * Container for organism data loaded from JSON.
 */
public record OrganismData(Map<String, String> speciesToSequence) {
    public void validate() throws IllegalArgumentException {
        if (speciesToSequence == null || speciesToSequence.isEmpty()) {
            throw new IllegalArgumentException("Organism data cannot be null or empty");
        }
    }
}