# src/clustering.py

from typing import Dict, List, Tuple
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform
from collections import defaultdict

def build_tree_from_scores(
    pairwise_scores: Dict[str, int],
    species_names: List[str]
) -> Tuple[np.ndarray, float]:
    """
    Builds a phylogenetic tree and returns the linkage matrix and max score.
    """
    num_species = len(species_names)
    if num_species < 2:
        raise ValueError("At least two species are required to build a tree.")

    max_score = float(max(pairwise_scores.values()) if pairwise_scores else 0)
    name_to_index = {name: i for i, name in enumerate(species_names)}
    distance_matrix = np.zeros((num_species, num_species))

    for pair_key, score in pairwise_scores.items():
        species1, species2 = pair_key.split('_')
        idx1 = name_to_index.get(species1)
        idx2 = name_to_index.get(species2)
        if idx1 is not None and idx2 is not None:
            distance = max_score - score
            distance_matrix[idx1, idx2] = distance
            distance_matrix[idx2, idx1] = distance

    condensed_distance_matrix = squareform(distance_matrix)
    linkage_matrix = linkage(condensed_distance_matrix, method='single')

    corrected_linkage_matrix = linkage_matrix.copy()
    corrected_linkage_matrix[:, 2] = max_score - corrected_linkage_matrix[:, 2]

    return corrected_linkage_matrix, max_score

def get_clusters_by_threshold(
    linkage_matrix: np.ndarray,
    species_names: List[str],
    threshold: int,
    max_score: float
) -> List[List[str]]:
    """Forms flat clusters from a hierarchical clustering by cutting the tree."""
    distance_threshold = max_score - threshold
    distance_linkage_matrix = linkage_matrix.copy()
    distance_linkage_matrix[:, 2] = max_score - distance_linkage_matrix[:, 2]

    cluster_ids = fcluster(
        distance_linkage_matrix,
        t=distance_threshold,
        criterion='distance'
    )

    clusters = defaultdict(list)
    for i, cluster_id in enumerate(cluster_ids):
        clusters[cluster_id].append(species_names[i])

    return list(clusters.values())

def _build_newick_recursive(
    node_id: int,
    linkage_matrix: np.ndarray,
    species_names: List[str],
    parent_height: float,
    with_distance: bool
) -> str:
    """Recursively builds a Newick format string for a given node."""
    num_species = len(species_names)
    if node_id < num_species:
        leaf_name = species_names[int(node_id)]
        if with_distance:
            branch_length = int(parent_height)
            return f"{leaf_name}:{branch_length}"
        return leaf_name

    merge_row = linkage_matrix[int(node_id) - num_species]
    child1_id, child2_id, current_height = merge_row[0], merge_row[1], merge_row[2]

    child1_str = _build_newick_recursive(child1_id, linkage_matrix, species_names, current_height, with_distance)
    child2_str = _build_newick_recursive(child2_id, linkage_matrix, species_names, current_height, with_distance)

    node_str = f"({child1_str},{child2_str})"
    if with_distance:
        branch_length = int(parent_height - current_height)
        node_str += f":{branch_length}"
    return node_str

def convert_tree_to_newick(
    linkage_matrix: np.ndarray,
    species_names: List[str],
    with_distance: bool = False
) -> str:
    """Converts a linkage matrix from SciPy into a Newick format string."""
    num_species = len(species_names)
    if linkage_matrix.shape[0] == 0:
        return "();"
    
    root_id = num_species + (num_species - 1) - 1
    root_height = linkage_matrix[-1, 2]
    newick_str = _build_newick_recursive(root_id, linkage_matrix, species_names, root_height, with_distance)
    return f"{newick_str};"