from pathlib import Path
from typing import List

import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster.hierarchy import dendrogram

def plot_dendrogram(Z: np.ndarray, labels: List[str], max_similarity: float, output_path: Path):
    """
    Generates and saves a horizontal dendrogram from a linkage matrix.
    The x-axis is transformed to represent the original similarity scores.
    """
    try:
        plt.figure(figsize=(12, max(8, len(labels) * 0.5)))
        
        dendrogram(Z, labels=labels, orientation='right', leaf_font_size=10)

        ax = plt.gca()
        current_ticks = ax.get_xticks()
        ax.set_xticklabels([int(max_similarity - tick) for tick in current_ticks])
        
        plt.title('Phylogenetic Tree (Hierarchical Clustering)', fontsize=16)
        plt.xlabel('Similarity Score (Needleman-Wunsch)', fontsize=12)
        plt.ylabel('Species', fontsize=12)
        plt.grid(axis='x', linestyle='--', alpha=0.6)
        plt.tight_layout()
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Dendrogram generated successfully at: {output_path}")
    except Exception as e:
        print(f"An error occurred during dendrogram generation: {e}")