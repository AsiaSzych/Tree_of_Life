# src/tree_builder.py
import numpy as np
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import linkage
import re
from typing import Dict, List, Tuple, Any

from src.utils import load_json_data

class PhylogeneticTreeBuilder:
    """
    A class to build a phylogenetic tree using agglomerative hierarchical clustering
    from Needleman-Wunsch similarity scores.
    """

    def __init__(self, scores_filepath: str):
        """
        Initializes the tree builder with the path to the pairwise similarity scores.

        Args:
            scores_filepath (str): Path to the JSON file containing pairwise
                                   Needleman-Wunsch similarity scores.
                                   Expected format: {"species1_species2": score, ...}
        """
        self.scores_filepath = scores_filepath
        self._species_labels: List[str] = []
        self._max_similarity_score: float = 0.0
        self._linkage_matrix: np.ndarray = np.array([])

    def _load_and_prepare_distances(self) -> np.ndarray:
        """
        Loads the flat similarity scores, identifies unique species,
        transforms similarity scores into distances, and returns a condensed
        distance vector suitable for scipy's linkage function.

        Returns:
            np.ndarray: A condensed distance vector.

        Raises:
            ValueError: If the scores file is empty or malformed.
        """
        print(f"Loading similarity scores from: {self.scores_filepath}")
        flat_scores = load_json_data(self.scores_filepath)

        if not isinstance(flat_scores, dict) or not flat_scores:
            raise ValueError(
                f"Invalid or empty scores data in '{self.scores_filepath}': "
                "Expected a non-empty dictionary."
            )

        # Extract all unique species names and sort them for consistent indexing
        species_set = set()
        all_similarity_values = []
        for key, score in flat_scores.items():
            if not isinstance(score, (int, float)):
                raise ValueError(f"Invalid score type for key '{key}': Expected a number.")
            
            parts = key.split('_')
            if len(parts) != 2:
                raise ValueError(f"Invalid key format '{key}': Expected 'species1_species2'.")
            
            species_set.add(parts[0])
            species_set.add(parts[1])
            all_similarity_values.append(score)

        self._species_labels = sorted(list(species_set))
        num_species = len(self._species_labels)
        species_to_idx = {name: i for i, name in enumerate(self._species_labels)}

        if not self._species_labels:
            raise ValueError("No species found in the scores file.")

        # Determine the maximum similarity score for distance transformation
        # This is crucial for mapping distances back to original similarity thresholds
        self._max_similarity_score = max(all_similarity_values)
        print(f"Determined maximum similarity score: {self._max_similarity_score}")

        # Initialize a square distance matrix
        distance_matrix = np.zeros((num_species, num_species), dtype=float)

        # Populate the distance matrix
        for key, similarity_score in flat_scores.items():
            s1, s2 = key.split('_')
            idx1, idx2 = species_to_idx[s1], species_to_idx[s2]

            # Transform similarity to distance: higher similarity -> lower distance
            distance = self._max_similarity_score - similarity_score

            distance_matrix[idx1, idx2] = distance
            distance_matrix[idx2, idx1] = distance # Ensure symmetry

        # Convert the square distance matrix to a condensed distance vector
        # This is the format expected by scipy.cluster.hierarchy.linkage
        condensed_distance_vector = squareform(distance_matrix)
        print(f"Prepared condensed distance vector for {num_species} species.")
        return condensed_distance_vector

    def build_tree(self) -> Tuple[np.ndarray, List[str], float]:
        """
        Builds the phylogenetic tree using single-linkage hierarchical clustering.

        Returns:
            Tuple[np.ndarray, List[str], float]:
                - linkage_matrix (np.ndarray): The hierarchical clustering linkage matrix (Z).
                                                Each row represents a merge: [cluster_id1, cluster_id2, distance, num_observations].
                - species_labels (List[str]): The ordered list of original species labels
                                              corresponding to the leaf nodes of the tree.
                - max_similarity_score (float): The maximum similarity score used for
                                                distance transformation. This is needed
                                                to convert linkage distances back to
                                                original similarity scores.
        """
        condensed_distances = self._load_and_prepare_distances()

        print("Performing single-linkage hierarchical clustering...")
        # Perform single-linkage clustering
        # 'method='single'' specifies single-linkage
        # 'metric='euclidean'' is the default, but since we provide precomputed distances,
        #   it's effectively using those.
        self._linkage_matrix = linkage(condensed_distances, method='single')
        print("Clustering complete. Linkage matrix generated.")

        return self._linkage_matrix, self._species_labels, self._max_similarity_score