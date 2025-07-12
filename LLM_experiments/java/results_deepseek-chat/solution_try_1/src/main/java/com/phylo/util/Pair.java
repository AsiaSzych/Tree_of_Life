package com.phylo.util;

/**
 * Immutable pair of elements for storing species combinations.
 * @param <T> Type of elements in pair
 */
public record Pair<T>(T first, T second) {
    @Override
    public String toString() {
        return "(" + first + ", " + second + ")";
    }
}