package com.phylo.util;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class UnionFind {
    private final int[] parent;
    private final int[] size;
    private int count;

    public UnionFind(int n) {
        parent = new int[n];
        size = new int[n];
        count = n;
        for (int i = 0; i < n; i++) {
            parent[i] = i;
            size[i] = 1;
        }
    }

    public int find(int p) {
        while (p != parent[p]) {
            parent[p] = parent[parent[p]];  // Path compression
            p = parent[p];
        }
        return p;
    }

    public void union(int p, int q) {
        int rootP = find(p);
        int rootQ = find(q);
        if (rootP == rootQ) return;

        // Union by size
        if (size[rootP] < size[rootQ]) {
            parent[rootP] = rootQ;
            size[rootQ] += size[rootP];
        } else {
            parent[rootQ] = rootP;
            size[rootP] += size[rootQ];
        }
        count--;
    }

    public List<List<String>> getClusters(List<String> elements) {
        Map<Integer, List<String>> clusterMap = new HashMap<>();
        for (int i = 0; i < parent.length; i++) {
            int root = find(i);
            clusterMap.computeIfAbsent(root, k -> new ArrayList<>())
                     .add(elements.get(i));
        }
        return new ArrayList<>(clusterMap.values());
    }
}