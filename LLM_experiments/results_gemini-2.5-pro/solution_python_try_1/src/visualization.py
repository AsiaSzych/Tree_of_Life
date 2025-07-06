# src/visualization.py

from pathlib import Path
from typing import List
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram

def plot_dendrogram(
    linkage_matrix: np.ndarray,
    species_names: List[str],
    output_path: Path
):
    """
    Generates and saves a horizontal dendrogram from a linkage matrix.
    """
    print(f"Generating dendrogram and saving to: {output_path}")
    try:
        plt.figure(figsize=(12, 8))
        dendrogram(
            linkage_matrix,
            labels=species_names,
            orientation='right',
            leaf_font_size=10,
        )
        plt.title('Phylogenetic Tree (Single Linkage)', fontsize=16)
        plt.xlabel('Needleman-Wunsch Similarity Score', fontsize=12)
        plt.grid(axis='x', linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        print(f"Successfully saved {output_path.name}.")
    except Exception as e:
        print(f"Error: Could not generate or save the dendrogram. Reason: {e}")
    finally:
        plt.close()