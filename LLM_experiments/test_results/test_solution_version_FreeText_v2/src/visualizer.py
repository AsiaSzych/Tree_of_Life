# src/visualizer.py
import os
import re
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram
import numpy as np
from typing import List

class DendrogramVisualizer:
    """
    A class to visualize phylogenetic trees as dendrograms.
    """

    def __init__(self, output_dir: str):
        """
        Initializes the DendrogramVisualizer.

        Args:
            output_dir (str): The directory where the dendrogram images should be saved.
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True) # Ensure output directory exists

    def draw_and_save_dendrogram(
        self,
        linkage_matrix: np.ndarray,
        species_labels: List[str],
        blosum_matrix_filepath: str,
        max_similarity_score: float
    ) -> str:
        """
        Draws a horizontal dendrogram and saves it as a PNG file.

        Args:
            linkage_matrix (np.ndarray): The hierarchical clustering linkage matrix (Z).
            species_labels (List[str]): The ordered list of original species labels.
            blosum_matrix_filepath (str): The path to the BLOSUM matrix file used,
                                          to determine the output filename.
            max_similarity_score (float): The maximum similarity score used for
                                          distance transformation. Used for axis labeling.

        Returns:
            str: The full path to the saved dendrogram image.
        """
        # Extract BLOSUM version from the filename
        match = re.search(r'blosum(\d+)\.json$', blosum_matrix_filepath)
        if not match:
            raise ValueError(
                f"Could not extract BLOSUM version from filename: {blosum_matrix_filepath}. "
                "Expected format like 'blosumXX.json'."
            )
        blosum_version = match.group(1)
        output_filename = f"phylogenetic_tree_blosum{blosum_version}.png"
        output_filepath = os.path.join(self.output_dir, output_filename)

        plt.figure(figsize=(12, 0.5 * len(species_labels))) # Adjust figure size dynamically
        plt.title(f"Phylogenetic Tree (BLOSUM{blosum_version})")
        plt.xlabel("Needleman-Wunsch Distance")
        plt.ylabel("Species")

        # Draw the dendrogram horizontally
        # The 'distance' values in linkage_matrix are already Max_Score - Actual_Score
        dendrogram(
            linkage_matrix,
            labels=species_labels,
            orientation='right', # Horizontal layout
            leaf_font_size=10,
            color_threshold=0, # Ensure all branches are colored
            above_threshold_color='black' # Default color for branches
        )

        # Optional: Add a secondary axis for original similarity scores
        # This can be helpful for interpretation, but might clutter small plots.
        # For now, let's stick to the primary request of NW distances on X-axis.
        # If needed, we can add:
        # ax2 = plt.gca().twiny()
        # ax2.set_xlim(plt.gca().get_xlim())
        # ax2.set_xticks(plt.gca().get_xticks())
        # ax2.set_xticklabels([f"{max_similarity_score - x:.0f}" for x in plt.gca().get_xticks()])
        # ax2.set_xlabel("Needleman-Wunsch Similarity Score")


        plt.tight_layout() # Adjust layout to prevent labels from overlapping
        plt.savefig(output_filepath)
        plt.close() # Close the plot to free up memory

        print(f"Dendrogram saved to: '{output_filepath}'")
        return output_filepath