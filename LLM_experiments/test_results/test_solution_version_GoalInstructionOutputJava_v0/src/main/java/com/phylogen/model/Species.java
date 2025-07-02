package com.phylogen.model;

/**
 * Represents a species with its name and DNA sequence.
 * Using a record for an immutable data carrier.
 *
 * @param name The common name of the species.
 * @param sequence The DNA sequence string.
 */
public record Species(String name, String sequence) {
}