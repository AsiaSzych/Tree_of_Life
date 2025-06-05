# src/cluster_analyzer.py
import os
import re
from collections import defaultdict
from typing import List, Dict, Any

import numpy as np
from scipy.cluster.hierarchy import fcluster

from src.utils import load_json_data, save_json_data

class ClusterAnalyzer:
    """
    A class to analyze and extract clusters from a hierarchical tree
    based on specified similarity thresholds.
    """

    def __init__(self, output_dir: str):
        """
        Initializes the ClusterAnalyzer.

        Args:
            output_dir (str): The directory where the cluster results JSON should be saved.
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True) # Ensure output directory exists

    def _load_thresholds(self, thresholds_filepath: str) -> List[float]:
        """
        Loads similarity thresholds from a text file.

        Args:
            thresholds_filepath (str): Path to the file containing thresholds (one per line).

        Returns:
            List[float]: A list of parsed similarity thresholds.

        Raises:
            ValueError: If a threshold cannot be converted to a float.
        """
        print(f"Loading thresholds from: {thresholds_filepath}")
        thresholds = []
        try:
            with open(thresholds_filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line: # Ignore empty lines
                        try:
                            thresholds.append(float(line))
                        except ValueError:
                            raise ValueError(f"Invalid threshold value '{line}' in '{thresholds_filepath}'. "
                                             "Thresholds must be numerical.")
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: Thresholds file not found at '{thresholds_filepath}'")
        except Exception as e:
            raise Exception(f"An unexpected error occurred while reading '{thresholds_filepath}': {e}")
        
        if not thresholds:
            print(f"Warning: No thresholds found in '{thresholds_filepath}'. No clusters will be generated.")

        return sorted(list(set(thresholds)), reverse=True) # Sort descending for consistent output, remove duplicates

    def find_and_save_clusters(
        self,
        linkage_matrix: np.ndarray,
        species_labels: List[str],
        max_similarity_score: float,
        thresholds_filepath: str,
        blosum_matrix_filepath: str
    ) -> str:
        """
        Finds clusters of species for each specified similarity threshold
        and saves the results to a JSON file.

        Args:
            linkage_matrix (np.ndarray): The hierarchical clustering linkage matrix (Z).
            species_labels (List[str]): The ordered list of original species labels.
            max_similarity_score (float): The maximum similarity score used for
                                          distance transformation.
            thresholds_filepath (str): Path to the file containing similarity thresholds.
            blosum_matrix_filepath (str): The path to the BLOSUM matrix file used,
                                          to determine the output filename.

        Returns:
            str: The full path to the saved clusters JSON file.
        """
        similarity_thresholds = self._load_thresholds(thresholds_filepath)
        
        if not similarity_thresholds:
            print("No thresholds to process. Skipping cluster generation.")
            return ""

        # Extract BLOSUM version for output filename
        match = re.search(r'blosum(\d+)\.json$', blosum_matrix_filepath)
        if not match:
            raise ValueError(
                f"Could not extract BLOSUM version from filename: {blosum_matrix_filepath}. "
                "Expected format like 'blosumXX.json'."
            )
        blosum_version = match.group(1)
        output_filename = f"clusters_for_blosum{blosum_version}.json"
        output_filepath = os.path.join(self.output_dir, output_filename)

        all_clusters_data: Dict[str, List[List[str]]] = {}

        print(f"\n--- Finding clusters for BLOSUM{blosum_version} ---")
        for sim_threshold in similarity_thresholds:
            # Convert similarity threshold to distance threshold
            # Remember: distance = Max_Score - Similarity_Score
            # So, a higher similarity threshold means a *lower* distance threshold
            dist_threshold = max_similarity_score - sim_threshold

            # Use fcluster to get cluster assignments
            # 'criterion='distance'' means cut the tree at the specified distance
            cluster_assignments = fcluster(linkage_matrix, dist_threshold, criterion='distance')

            # Map cluster IDs to species names
            clusters_by_id: Dict[int, List[str]] = defaultdict(list)
            for i, cluster_id in enumerate(cluster_assignments):
                clusters_by_id[cluster_id].append(species_labels[i])

            # Convert to list of lists format
            current_clusters: List[List[str]] = sorted([sorted(members) for members in clusters_by_id.values()])

            # Store and print results
            threshold_key = f"{sim_threshold:.0f}" # Use integer string for key if scores are integers
            all_clusters_data[threshold_key] = current_clusters

            print(f"\nClusters for Similarity Threshold: {sim_threshold} (Distance Threshold: {dist_threshold:.2f})")
            for cluster in current_clusters:
                print(f"  - {', '.join(cluster)}")

        save_json_data(all_clusters_data, output_filepath)
        print(f"\nAll clusters saved to: '{output_filepath}'")
        return output_filepath
