package com.example.phylo;

import java.util.Objects;

// Immutable, unordered pair for storing species pairs
public class Pair<T extends Comparable<T>, U extends Comparable<U>> {
    private final T first;
    private final U second;

    public Pair(T a, U b) {
        if (a.compareTo((T) b) <= 0) {
            this.first = a;
            this.second = b;
        } else {
            this.first = (T)b;
            this.second = (U)a;
        }
    }

    public T getFirst() {
        return first;
    }

    public U getSecond() {
        return second;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Pair<?, ?> pair)) return false;
        return Objects.equals(first, pair.first) && Objects.equals(second, pair.second);
    }

    @Override
    public int hashCode() {
        return Objects.hash(first, second);
    }
}