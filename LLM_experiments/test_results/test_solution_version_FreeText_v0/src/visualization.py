# src/visualization.py

import os
import numpy as np
from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt
from typing import List

def draw_and_save_dendrogram(
    linkage_matrix: np.ndarray,
    species_labels: List[str],
    output_filepath: str,
    title: str = "Phylogenetic Tree Dendrogram"
) -> None:
    """
    Draws a horizontal dendrogram and saves it to a PNG file.

    Args:
        linkage_matrix (np.ndarray): The linkage matrix (Z) from scipy.cluster.hierarchy.linkage.
        species_labels (List[str]): A list of labels for the leaf nodes (species names).
        output_filepath (str): The full path to the output PNG file.
        title (str, optional): The title for the dendrogram plot.
    """
    try:
        output_dir = os.path.dirname(output_filepath)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        fig_height = max(6, 0.3 * len(species_labels))
        plt.figure(figsize=(12, fig_height))
        plt.title(title)
        plt.xlabel("Needleman-Wunsch Distance")
        plt.ylabel("Species")

        dendrogram(
            linkage_matrix,
            labels=species_labels,
            orientation='left',
            leaf_font_size=10,
            leaf_rotation=0,
            show_contracted=True
        )

        plt.tight_layout()
        plt.savefig(output_filepath, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Successfully saved dendrogram to: {output_filepath}")
    except Exception as e:
        print(f"Error drawing or saving dendrogram to {output_filepath}: {e}")
        raise