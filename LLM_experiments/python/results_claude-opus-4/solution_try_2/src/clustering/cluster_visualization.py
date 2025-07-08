"""
Visualization utilities for clustering results.
"""
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, List
import json


def plot_cluster_size_distribution(
    clusters_by_threshold: Dict[int, List[List[str]]],
    blosum_version: str,
    output_dir: str = "."
) -> str:
    """
    Plot distribution of cluster sizes across different thresholds.
    
    Args:
        clusters_by_threshold: Dictionary mapping thresholds to clusters
        blosum_version: BLOSUM version used
        output_dir: Directory to save output file
        
    Returns:
        Path to saved plot
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    thresholds = sorted(clusters_by_threshold.keys())
    num_clusters = []
    avg_sizes = []
    
    for threshold in thresholds:
        clusters = clusters_by_threshold[threshold]
        num_clusters.append(len(clusters))
        
        if clusters:
            avg_size = sum(len(c) for c in clusters) / len(clusters)
            avg_sizes.append(avg_size)
        else:
            avg_sizes.append(0)
    
    # Create two y-axes
    ax2 = ax.twinx()
    
    # Plot number of clusters
    line1 = ax.plot(thresholds, num_clusters, 'b-o', linewidth=2, 
                    markersize=8, label='Number of Clusters')
    ax.set_xlabel('Threshold', fontsize=12)
    ax.set_ylabel('Number of Clusters', fontsize=12, color='b')
    ax.tick_params(axis='y', labelcolor='b')
    
    # Plot average cluster size
    line2 = ax2.plot(thresholds, avg_sizes, 'r-s', linewidth=2, 
                     markersize=8, label='Average Cluster Size')
    ax2.set_ylabel('Average Cluster Size', fontsize=12, color='r')
    ax2.tick_params(axis='y', labelcolor='r')
    
    # Add title and grid
    ax.set_title(f'Clustering Analysis ({blosum_version.upper()})', 
                fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Add legend
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax.legend(lines, labels, loc='center right')
    
    plt.tight_layout()
    
    # Save figure
    filename = f"cluster_analysis_{blosum_version}.png"
    filepath = Path(output_dir) / filename
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close(fig)
    
    print(f"Saved cluster analysis plot to: {filepath}")
    return str(filepath)