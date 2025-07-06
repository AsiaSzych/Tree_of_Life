package com.mycompany.phylogeny.domain;

/**
 * Represents a species with its name and amino acid sequence.
 * Using a record for immutability and conciseness.
 *
 * @param name The name of the species.
 * @param sequence The amino acid sequence string.
 */
public record Species(String name, String sequence) {}
