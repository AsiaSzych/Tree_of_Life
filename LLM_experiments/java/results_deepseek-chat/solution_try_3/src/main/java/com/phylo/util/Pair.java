package com.phylo.util;

import java.util.Objects;

/**
 * Immutable pair for storing species pairs.
 */
public record Pair<T>(T first, T second) {
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Pair<?> pair = (Pair<?>) o;
        return (Objects.equals(first, pair.first) && Objects.equals(second, pair.second)) ||
               (Objects.equals(first, pair.second) && Objects.equals(second, pair.first));
    }

    @Override
    public int hashCode() {
        return Objects.hash(first) + Objects.hash(second);
    }
}
