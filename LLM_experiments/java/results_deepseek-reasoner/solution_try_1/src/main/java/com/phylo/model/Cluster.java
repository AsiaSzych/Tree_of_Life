package com.phylo.model;

import java.util.List;

public class Cluster {
    private final PhyloNode node;
    private final String id;
    
    public Cluster(PhyloNode node) {
        this.node = node;
        this.id = node.getId();
    }
    
    public PhyloNode getNode() { return node; }
    public String getId() { return id; }
    public List<String> getSpecies() { return node.getSpecies(); }
}