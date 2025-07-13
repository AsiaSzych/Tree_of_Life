package com.phylogenetics.model;

/**
 * Represents an organism with its amino acid sequence.
 */
public record Organism(String name, String sequence) {
    public Organism {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("Organism name cannot be null or blank");
        }
        if (sequence == null) {
            throw new IllegalArgumentException("Sequence cannot be null");
        }
    }
}