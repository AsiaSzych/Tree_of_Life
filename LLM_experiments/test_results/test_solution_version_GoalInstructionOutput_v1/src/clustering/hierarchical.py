import itertools
from typing import Dict, List, Tuple
from collections import defaultdict

import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster

def build_tree(scores: Dict[str, Dict[str, int]], labels: List[str]) -> Tuple[np.ndarray, float]:
    """Builds a hierarchical tree using single-linkage clustering on similarity scores."""
    if not scores: return np.array([]), 0.0
    max_similarity = float(max(score for inner in scores.values() for score in inner.values()))

    distances = [max_similarity - scores[s1][s2] for s1, s2 in itertools.combinations(labels, 2)]
    if not distances: return np.array([]), max_similarity

    condensed_matrix = np.array(distances, dtype=float)
    Z = linkage(condensed_matrix, method='single')
    return Z, max_similarity

def to_newick(Z: np.ndarray, labels: List[str], with_distance: bool = False) -> str:
    """Converts a SciPy linkage matrix into a Newick format string."""
    n = len(labels)
    if Z.shape[0] != n - 1: raise ValueError("Invalid linkage matrix.")

    node_heights = {i: 0 for i in range(n)}
    for i, row in enumerate(Z): node_heights[n + i] = row[2]

    branch_lengths = {}
    if with_distance:
        for i, row in enumerate(Z):
            parent_id, parent_height = n + i, node_heights[n + i]
            c1_id, c2_id = int(row[0]), int(row[1])
            branch_lengths[c1_id] = parent_height - node_heights[c1_id]
            branch_lengths[c2_id] = parent_height - node_heights[c2_id]

    root_node_id = n + Z.shape[0] - 1
    newick_str = _build_newick_recursive(root_node_id, Z, labels, n, with_distance, branch_lengths)
    return f"{newick_str};"

def _build_newick_recursive(node_id, Z, labels, n_leaves, with_dist, branch_lengths) -> str:
    """Recursive helper to build the Newick string for a given node."""
    if node_id < n_leaves:
        name = labels[node_id]
        return f"{name}:{int(branch_lengths.get(node_id, 0))}" if with_dist else name

    row = Z[node_id - n_leaves]
    c1_str = _build_newick_recursive(int(row[0]), Z, labels, n_leaves, with_dist, branch_lengths)
    c2_str = _build_newick_recursive(int(row[1]), Z, labels, n_leaves, with_dist, branch_lengths)
    
    subtree = f"({c1_str},{c2_str})"
    return f"{subtree}:{int(branch_lengths.get(node_id, 0))}" if with_dist else subtree

def get_clusters_by_threshold(Z: np.ndarray, labels: List[str], sim_thresh: int, max_sim: float) -> List[List[str]]:
    """Forms flat clusters from a hierarchical tree based on a similarity threshold."""
    dist_thresh = max_sim - sim_thresh
    cluster_ids = fcluster(Z, t=dist_thresh, criterion='distance')
    
    clusters = defaultdict(list)
    for i, cluster_id in enumerate(cluster_ids):
        clusters[cluster_id].append(labels[i])
    return list(clusters.values())