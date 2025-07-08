"""
Utility functions for dendrogram visualization.
"""
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Tuple
from src.tree.phylogenetic_tree import PhylogeneticTree


def create_dendrogram_with_clusters(
    tree: PhylogeneticTree,
    threshold: int,
    blosum_version: str,
    output_dir: str = ".",
    figsize: Tuple[int, int] = (12, 8)
) -> str:
    """
    Create dendrogram with cluster coloring at a specific threshold.
    
    Args:
        tree: PhylogeneticTree object
        threshold: Similarity threshold for clustering
        blosum_version: BLOSUM version used
        output_dir: Directory to save output file
        figsize: Figure size
        
    Returns:
        Path to saved file
    """
    from .dendrogram import DendrogramDrawer
    
    # Get clusters at threshold
    clusters = tree.get_clusters_at_threshold(threshold)
    
    # Create color map for clusters
    colors = plt.cm.Set3(np.linspace(0, 1, len(clusters)))
    cluster_colors = {}
    
    for i, cluster in enumerate(clusters):
        for species in cluster:
            cluster_colors[species] = colors[i]
    
    # Create dendrogram
    drawer = DendrogramDrawer(tree)
    
    # Assign positions
    drawer._assign_leaf_positions(tree.root)
    drawer._calculate_node_positions(tree.root)
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Draw tree
    drawer._draw_node(ax, tree.root)
    
    # Add colored leaf labels
    for leaf_name, y_pos in drawer.leaf_positions.items():
        color = cluster_colors.get(leaf_name, 'black')
        ax.text(drawer.max_similarity * 1.02, y_pos, leaf_name, 
               va='center', fontsize=10, color=color, weight='bold')
    
    # Add threshold line
    ax.axvline(x=threshold, color='red', linestyle='--', linewidth=2, alpha=0.7)
    ax.text(threshold, ax.get_ylim()[1] * 0.95, f'Threshold: {threshold}', 
           ha='center', va='top', color='red', fontsize=10, weight='bold')
    
    # Set axis properties
    ax.set_xlim(-drawer.max_similarity * 0.05, drawer.max_similarity * 1.15)
    ax.set_ylim(-0.5, len(drawer.leaf_positions) - 0.5)
    ax.set_xlabel('Needleman-Wunsch Similarity Score', fontsize=12)
    ax.set_ylabel('Species', fontsize=12)
    ax.set_yticks([])
    ax.grid(True, axis='x', alpha=0.3)
    ax.invert_xaxis()
    
    # Add title
    title = f"Phylogenetic Tree with Clusters ({blosum_version.upper()}, threshold={threshold})"
    ax.set_title(title, fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    
    # Save figure
    filename = f"phylogenetic_tree_{blosum_version}_clusters_{threshold}.png"
    filepath = Path(output_dir) / filename
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close(fig)
    
    print(f"Saved clustered dendrogram to: {filepath}")
    return str(filepath)


def plot_similarity_distribution(
    tree: PhylogeneticTree,
    blosum_version: str,
    output_dir: str = "."
) -> str:
    """
    Plot distribution of similarity scores in the tree.
    
    Args:
        tree: PhylogeneticTree object
        blosum_version: BLOSUM version used
        output_dir: Directory to save output file
        
    Returns:
        Path to saved file
    """
    # Get all merge heights
    merge_history = tree.get_merge_history()
    heights = [height for _, _, height in merge_history]
    
    # Create histogram
    fig, ax = plt.subplots(figsize=(10, 6))
    
    n_bins = min(30, len(heights))
    ax.hist(heights, bins=n_bins, edgecolor='black', alpha=0.7)
    
    ax.set_xlabel('Needleman-Wunsch Similarity Score', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.set_title(f'Distribution of Merge Heights ({blosum_version.upper()})', 
                fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Add statistics
    mean_height = np.mean(heights)
    median_height = np.median(heights)
    ax.axvline(mean_height, color='red', linestyle='--', linewidth=2, 
              label=f'Mean: {mean_height:.0f}')
    ax.axvline(median_height, color='green', linestyle='--', linewidth=2, 
              label=f'Median: {median_height:.0f}')
    ax.legend()
    
    plt.tight_layout()
    
    # Save figure
    filename = f"similarity_distribution_{blosum_version}.png"
    filepath = Path(output_dir) / filename
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close(fig)
    
    print(f"Saved similarity distribution to: {filepath}")
    return str(filepath)