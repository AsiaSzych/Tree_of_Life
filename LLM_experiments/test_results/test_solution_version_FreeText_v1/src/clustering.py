# src/clustering.py

import numpy as np
from scipy.cluster.hierarchy import fcluster # New import for clustering
from typing import List, Dict, Any
import os

def load_thresholds(filepath: str) -> List[float]:
    """
    Loads clustering thresholds from a text file, one float value per line.

    Args:
        filepath (str): The path to the thresholds.txt file.

    Returns:
        List[float]: A list of numerical thresholds.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If a line in the file cannot be converted to a float.
        Exception: For other unexpected I/O errors.
    """
    thresholds: List[float] = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                stripped_line = line.strip()
                if not stripped_line: # Skip empty lines
                    continue
                try:
                    thresholds.append(float(stripped_line))
                except ValueError:
                    raise ValueError(
                        f"Error: Invalid threshold value '{stripped_line}' "
                        f"on line {line_num} in '{filepath}'. "
                        "Each line must contain a valid number."
                    )
        return thresholds
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: Thresholds file not found at '{filepath}'")
    except Exception as e:
        raise Exception(f"An unexpected error occurred while reading '{filepath}': {e}")


def get_clusters_at_threshold(
    linkage_matrix: np.ndarray,
    species_labels: List[str],
    threshold: float
) -> List[List[str]]:
    """
    Identifies clusters of species by cutting the hierarchical tree at a given distance threshold.

    Args:
        linkage_matrix (np.ndarray): The hierarchical clustering linkage matrix (Z-matrix).
        species_labels (List[str]): A sorted list of original species names, corresponding
                                   to the leaf nodes in the linkage matrix.
        threshold (float): The distance threshold at which to cut the tree.

    Returns:
        List[List[str]]: A list of lists, where each inner list represents a cluster
                         of species names.
    """
    # fcluster returns an array where each element is the cluster ID for the corresponding observation.
    # criterion='distance' means clusters are formed such that all observations within a cluster
    # are within 't' (threshold) distance of each other.
    cluster_assignments = fcluster(linkage_matrix, t=threshold, criterion='distance')

    # Create a dictionary to group species by their cluster ID
    clusters_dict: Dict[int, List[str]] = {}
    for i, cluster_id in enumerate(cluster_assignments):
        if cluster_id not in clusters_dict:
            clusters_dict[cluster_id] = []
        clusters_dict[cluster_id].append(species_labels[i])

    # Convert the dictionary values (lists of species) into a list of lists
    # Sort clusters by the first species name for consistent output
    sorted_clusters = sorted(clusters_dict.values(), key=lambda x: sorted(x)[0])

    return sorted_clusters