# src/clustering.py

import itertools
from collections import defaultdict
from typing import Dict, List, Any

import numpy as np
from scipy.cluster.hierarchy import linkage, to_tree, dendrogram, fcluster
import matplotlib.pyplot as plt

def build_tree(
    similarity_matrix: Dict[str, Dict[str, int]],
    species_names: List[str]
) -> Dict[str, Any]:
    """
    Builds a phylogenetic tree using agglomerative hierarchical clustering.
    """
    all_scores = [
        similarity_matrix[s1][s2]
        for s1, s2 in itertools.combinations(species_names, 2)
    ]
    if not all_scores:
        return {
            'linkage_matrix_sim': np.array([]),
            'linkage_matrix_dist': np.array([]),
            'labels': species_names,
            'max_similarity': 0
        }
        
    max_similarity = max(all_scores)

    condensed_distance_matrix = [
        max_similarity - similarity_matrix[s1][s2]
        for s1, s2 in itertools.combinations(species_names, 2)
    ]

    if not condensed_distance_matrix:
        return {
            'linkage_matrix_sim': np.array([]),
            'linkage_matrix_dist': np.array([]),
            'labels': species_names,
            'max_similarity': max_similarity
        }

    linkage_matrix_dist = linkage(
        condensed_distance_matrix, method='single', metric='euclidean'
    )

    linkage_matrix_sim = linkage_matrix_dist.copy()
    linkage_matrix_sim[:, 2] = max_similarity - linkage_matrix_dist[:, 2]

    return {
        'linkage_matrix_sim': linkage_matrix_sim,
        'linkage_matrix_dist': linkage_matrix_dist,
        'labels': species_names,
        'max_similarity': max_similarity
    }

def to_newick(tree_data: Dict[str, Any], with_distance: bool = False) -> str:
    """
    Converts a tree from linkage matrix format to a Newick string.
    """
    linkage_matrix = tree_data.get('linkage_matrix_dist')
    if linkage_matrix is None or linkage_matrix.shape[0] == 0:
        return ";".join([f"({label})" for label in tree_data['labels']]) + ";" if tree_data['labels'] else ";"

    labels = tree_data['labels']
    root = to_tree(linkage_matrix, rd=False)

    def _build_newick_recursive(node, parent_dist):
        if node.is_leaf():
            label = labels[node.id]
            if with_distance:
                branch_length = parent_dist - 0.0
                return f"{label}:{branch_length:.10f}"
            return label
        
        left_str = _build_newick_recursive(node.left, node.dist)
        right_str = _build_newick_recursive(node.right, node.dist)
        newick_str = f"({left_str},{right_str})"
        
        if with_distance:
            branch_length = parent_dist - node.dist
            return f"{newick_str}:{branch_length:.10f}"
        return newick_str

    newick_string = _build_newick_recursive(root, root.dist)
    return f"{newick_string};"

def draw_dendrogram(tree_data: Dict[str, Any], output_path: str):
    """
    Draws a horizontal dendrogram and saves it to a file.
    """
    linkage_matrix = tree_data.get('linkage_matrix_sim')
    if linkage_matrix is None or linkage_matrix.shape[0] == 0:
        print("Warning: Cannot draw dendrogram for an empty or trivial tree.")
        return

    fig, ax = plt.subplots(figsize=(12, 8))
    dendrogram(
        linkage_matrix,
        labels=tree_data['labels'],
        orientation='right',
        ax=ax
    )
    ax.set_title('Phylogenetic Tree Dendrogram', fontsize=16)
    ax.set_xlabel('Needleman-Wunsch Similarity Score', fontsize=12)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close(fig)

def get_clusters_at_threshold(
    tree_data: Dict[str, Any],
    similarity_threshold: float
) -> List[List[str]]:
    """
    Forms clusters from a phylogenetic tree at a given similarity threshold.
    """
    linkage_matrix_dist = tree_data.get('linkage_matrix_dist')
    if linkage_matrix_dist is None or linkage_matrix_dist.shape[0] == 0:
        return [[label] for label in tree_data['labels']]

    max_similarity = tree_data['max_similarity']
    distance_threshold = max_similarity - similarity_threshold

    cluster_ids = fcluster(
        linkage_matrix_dist,
        t=distance_threshold,
        criterion='distance'
    )

    clusters = defaultdict(list)
    for i, cluster_id in enumerate(cluster_ids):
        clusters[cluster_id].append(tree_data['labels'][i])

    return list(clusters.values())