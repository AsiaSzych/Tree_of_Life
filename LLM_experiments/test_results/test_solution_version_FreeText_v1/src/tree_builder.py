# src/tree_builder.py

import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram # dendrogram added
from scipy.spatial.distance import squareform
from typing import Dict, List, Tuple
import os
from Bio import Phylo
import matplotlib.pyplot as plt # New import for plotting

def _convert_similarity_to_distance_matrix(
    pairwise_similarity_scores: Dict[str, int],
    species_names: List[str]
) -> np.ndarray:
    """
    Converts a dictionary of pairwise similarity scores into a condensed distance matrix
    suitable for SciPy's hierarchical clustering functions.

    The distance is calculated as: max_overall_similarity_score - current_similarity_score.
    This ensures that higher similarity corresponds to lower distance, which is required
    by distance-based clustering algorithms.

    Args:
        pairwise_similarity_scores (Dict[str, int]): A dictionary where keys are
                                                      "species1_species2" (canonical form)
                                                      and values are their Needleman-Wunsch
                                                      similarity scores. Assumes keys like
                                                      "A_A" are present for self-similarity.
        species_names (List[str]): A sorted list of all unique species names,
                                   defining the order for the distance matrix.

    Returns:
        np.ndarray: A condensed distance matrix (1D array) as expected by
                    scipy.cluster.hierarchy.linkage.

    Raises:
        ValueError: If no pairwise similarity scores are provided, or if a required
                    pairwise score is missing for a pair of species.
    """
    num_species = len(species_names)

    if not pairwise_similarity_scores:
        raise ValueError("No pairwise similarity scores provided to build the distance matrix.")

    # Find the maximum similarity score across all pairs.
    # This is crucial for normalizing similarities into distances.
    max_similarity_score = max(pairwise_similarity_scores.values())

    # Create a mapping from species name to its index for efficient lookup
    species_to_index = {name: i for i, name in enumerate(species_names)}

    # Initialize a square matrix to hold full distances temporarily.
    # This makes population easier before converting to condensed form.
    full_distance_matrix = np.zeros((num_species, num_species))

    for i in range(num_species):
        for j in range(num_species):
            s1 = species_names[i]
            s2 = species_names[j]

            if s1 == s2:
                # Distance for self-alignment is always 0
                full_distance_matrix[i, j] = 0
            else:
                # Create canonical key for lookup (e.g., "A_B" not "B_A")
                key = f"{min(s1, s2)}_{max(s1, s2)}"
                score = pairwise_similarity_scores.get(key)

                if score is None:
                    raise ValueError(f"Missing similarity score for pair: {s1}_{s2}. "
                                     f"Ensure '{key}' exists in the input scores dictionary.")

                # Convert similarity to distance: higher similarity -> lower distance
                full_distance_matrix[i, j] = max_similarity_score - score

    # Convert the square distance matrix to a condensed (1D) form.
    # This is the format required by scipy.cluster.hierarchy.linkage.
    condensed_distance_matrix = squareform(full_distance_matrix)

    return condensed_distance_matrix


def build_phylogenetic_tree(
    organisms_data: Dict[str, str],
    pairwise_scores: Dict[str, int]
) -> Tuple[np.ndarray, List[str], int]:
    """
    Builds a phylogenetic tree using single-linkage hierarchical clustering
    based on Needleman-Wunsch similarity scores.

    Args:
        organisms_data (Dict[str, str]): A dictionary of species names and their DNA sequences.
                                         Used to get the ordered list of species names.
        pairwise_scores (Dict[str, int]): A dictionary of Needleman-Wunsch similarity scores
                                          for all unique pairs of species (e.g., "species1_species2": score).

    Returns:
        Tuple[np.ndarray, List[str], int]:
            - linkage_matrix (np.ndarray): The hierarchical clustering linkage matrix (Z-matrix).
                                           Each row [idx1, idx2, distance, num_obs] represents a merge.
                                           'distance' here is (max_similarity - merge_similarity).
            - species_labels (List[str]): A sorted list of original species names,
                                          corresponding to the indices in the linkage matrix.
            - max_similarity_score (int): The maximum similarity score found in the input,
                                          used for converting linkage distances back to similarities
                                          for interpreting merge points.
    """
    # Ensure species names are sorted consistently for indexing.
    # This order will correspond to the leaf nodes in the linkage matrix.
    species_labels = sorted(list(organisms_data.keys()))

    # Convert similarity scores to a condensed distance matrix
    condensed_distances = _convert_similarity_to_distance_matrix(
        pairwise_scores, species_labels
    )

    # Find the maximum similarity score for later conversion of linkage distances
    # back to the original similarity scale if needed for interpretation.
    max_similarity_score = max(pairwise_scores.values())

    # Perform single-linkage hierarchical clustering.
    # 'single' method means the distance between two clusters is the minimum distance
    # between any two observations in the different clusters.
    # Since we converted similarity to distance (max_sim - sim),
    # min_distance in the linkage matrix corresponds to max_similarity in the original scores,
    # which aligns with the requirement to merge the most similar pairs first.
    linkage_matrix = linkage(condensed_distances, method='single')

    return linkage_matrix, species_labels, max_similarity_score


def export_tree_to_newick(
    linkage_matrix: np.ndarray,
    species_labels: List[str],
    output_dir: str,
    blosum_suffix: str
) -> None:
    """
    Exports the phylogenetic tree represented by the linkage matrix to Newick format files.
    Generates two versions: one with only node names, and one with names and branch lengths.

    Args:
        linkage_matrix (np.ndarray): The hierarchical clustering linkage matrix (Z-matrix).
        species_labels (List[str]): A sorted list of original species names.
        output_dir (str): The directory where the Newick files will be saved.
        blosum_suffix (str): The BLOSUM version suffix (e.g., "50" or "62") for filenames.
    """
    os.makedirs(output_dir, exist_ok=True)

    # 1. Create Biopython Tree object from linkage matrix
    # Phylo.from_linkage correctly interprets the linkage matrix distances as node heights
    # and calculates branch lengths as differences in heights.
    tree_with_distances = Phylo.from_linkage(linkage_matrix, species_labels)

    # 2. Export tree with distances
    filepath_with_distances = os.path.join(output_dir, f"tree{blosum_suffix}_newick_with_distance.nw")
    try:
        Phylo.write(tree_with_distances, filepath_with_distances, "newick")
        print(f"Tree with distances saved to '{filepath_with_distances}'.")
    except Exception as e:
        print(f"Error saving tree with distances to Newick: {e}")

    # 3. Export tree without distances
    # Create a deep copy to modify branch lengths without affecting the original tree object
    tree_names_only = tree_with_distances.copy()
    for clade in tree_names_only.find_clades():
        clade.branch_length = None # Remove branch lengths for names-only format

    filepath_names_only = os.path.join(output_dir, f"tree{blosum_suffix}_newick.nw")
    try:
        Phylo.write(tree_names_only, filepath_names_only, "newick")
        print(f"Tree (names only) saved to '{filepath_names_only}'.")
    except Exception as e:
        print(f"Error saving tree (names only) to Newick: {e}")


def draw_and_save_dendrogram(
    linkage_matrix: np.ndarray,
    species_labels: List[str],
    output_dir: str,
    blosum_suffix: str
) -> None:
    """
    Draws a horizontal dendrogram of the phylogenetic tree and saves it as a PNG image.

    Args:
        linkage_matrix (np.ndarray): The hierarchical clustering linkage matrix (Z-matrix).
        species_labels (List[str]): A sorted list of original species names.
        output_dir (str): The directory where the dendrogram image will be saved.
        blosum_suffix (str): The BLOSUM version suffix (e.g., "50" or "62") for the filename.
    """
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"phylogenetic_tree_blosum{blosum_suffix}.png")

    try:
        # Determine figure size dynamically based on number of species for better readability
        # A rough heuristic: 0.5 inch per species for height, fixed width.
        fig_height = max(6, len(species_labels) * 0.5)
        plt.figure(figsize=(12, fig_height)) # Width, Height

        # Create the dendrogram
        # orientation='right' makes it horizontal with distances on the x-axis
        # labels=species_labels assigns the species names to the leaf nodes
        dendrogram(
            linkage_matrix,
            orientation='right',
            labels=species_labels,
            leaf_font_size=10, # Adjust font size for labels
            leaf_rotation=0,   # Keep labels horizontal
            color_threshold=0, # Color all branches black initially, or set a threshold for coloring clusters
            above_threshold_color='black'
        )

        plt.title(f"Phylogenetic Tree (BLOSUM{blosum_suffix})")
        plt.xlabel("Needleman-Wunsch Distance (Max Score - NW Score)")
        plt.ylabel("Species")
        plt.grid(axis='x', linestyle='--', alpha=0.7) # Add a grid for easier distance reading
        plt.tight_layout() # Adjust layout to prevent labels from overlapping

        plt.savefig(filepath, dpi=300) # Save with high resolution
        plt.close() # Close the plot to free up memory
        print(f"Dendrogram saved to '{filepath}'.")
    except Exception as e:
        print(f"Error drawing or saving dendrogram: {e}")
