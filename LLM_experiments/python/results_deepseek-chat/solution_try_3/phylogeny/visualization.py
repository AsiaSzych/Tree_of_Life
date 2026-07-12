"""Dendrogram visualization for phylogenetic trees."""

import matplotlib.pyplot as plt
from typing import Dict, Optional
from .tree import TreeNode

def plot_dendrogram(
    tree: TreeNode,
    blosum_version: str,
    output_dir: str = ".",
    dpi: int = 300
) -> None:
    """Generate and save a horizontal dendrogram.
    
    Args:
        tree: Root node of the phylogenetic tree
        blosum_version: BLOSUM matrix version (50 or 62)
        output_dir: Directory to save the image
        dpi: Image resolution in dots per inch
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Recursive function to calculate positions
    def _plot_node(node, x_pos, y_pos, y_scale):
        if node.is_leaf():
            ax.text(x_pos, y_pos, node.name, 
                   ha='right', va='center')
            return {
                'x': x_pos,
                'y': y_pos,
                'name': node.name
            }
        
        left = _plot_node(node.left, x_pos, y_pos - y_scale, y_scale/2)
        right = _plot_node(node.right, x_pos, y_pos + y_scale, y_scale/2)
        
        # Draw horizontal line (using NW score for x position)
        ax.plot([left['x'], node.height], [left['y'], left['y']], 'k-')
        ax.plot([right['x'], node.height], [right['y'], right['y']], 'k-')
        
        # Draw vertical connecting line
        ax.plot([node.height, node.height], [left['y'], right['y']], 'k-')
        
        return {
            'x': node.height,
            'y': (left['y'] + right['y']) / 2
        }
    
    # Start plotting from root
    _plot_node(tree, tree.height, 0, 5)
    
    # Style the plot
    ax.set_xlabel('Needleman-Wunsch Similarity Score')
    ax.set_title(f'Phylogenetic Tree (BLOSUM{blosum_version})')
    ax.yaxis.set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # Save to file
    output_path = f"{output_dir}/phylogenetic_tree_blosum{blosum_version}.png"
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
    plt.close()