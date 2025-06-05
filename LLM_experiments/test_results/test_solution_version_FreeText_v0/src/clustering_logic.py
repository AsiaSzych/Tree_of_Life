# src/clustering_logic.py

import numpy as np
from scipy.cluster.hierarchy import fcluster
from typing import List, Dict

def extract_clusters(
    linkage_matrix: np.ndarray,
    species_labels: List[str],
    threshold: float
) -> List[List[str]]:
    """
    Extracts clusters of species from the linkage matrix at a given distance threshold.

    Args:
        linkage_matrix (np.ndarray): The linkage matrix (Z) from scipy.cluster.hierarchy.linkage.
        species_labels (List[str]): A list of labels for the leaf nodes (species names),
                                    in the order corresponding to the original data.
        threshold (float): The distance threshold at which to cut the dendrogram.

    Returns:
        List[List[str]]: A list of lists, where each inner list contains the names of species
                         belonging to a single cluster.
    """
    cluster_assignments = fcluster(linkage_matrix, threshold, criterion='distance')

    clusters_dict: Dict[int, List[str]] = {}
    for i, cluster_id in enumerate(cluster_assignments):
        if cluster_id not in clusters_dict:
            clusters_dict[cluster_id] = []
        clusters_dict[cluster_id].append(species_labels[i])

    sorted_clusters = sorted(clusters_dict.values(), key=lambda x: x[0])
    return sorted_clusters