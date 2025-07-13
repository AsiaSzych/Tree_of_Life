package com.phylo.model;

/**
 * Represents a pair of clusters with their similarity score.
 */
public record ClusterPair(PhylogeneticNode cluster1, PhylogeneticNode cluster2, double similarity) 
    implements Comparable<ClusterPair> {
    @Override
    public int compareTo(ClusterPair other) {
        return Double.compare(other.similarity, this.similarity); // Descending order
    }
}