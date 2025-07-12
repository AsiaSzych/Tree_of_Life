import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, Tuple
from tree.node import TreeNode

def plot_dendrogram(tree_root: TreeNode, blosum_type: str, output_dir: str = "./output"):
    """
    Plot and save a horizontal dendrogram with NW scores as x-axis.
    
    Args:
        tree_root: Root node of the phylogenetic tree
        blosum_type: BLOSUM matrix version (50 or 62)
        output_dir: Directory to save the plot (default: ./output)
    """
    Path(output_dir).mkdir(exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Recursive function to plot nodes
    def _plot_node(node, y, y_step):
        if node.is_leaf():
            ax.text(node.height + 0.02 * max_height, y, node.name, 
                   ha='left', va='center', fontsize=10)
            return y
        
        # Plot left and right branches
        left_y = _plot_node(node.left, y, y_step/2)
        right_y = _plot_node(node.right, y + y_step, y_step/2)
        
        # Draw horizontal lines (NW scores)
        ax.hlines(y=left_y, xmin=node.left.height, xmax=node.height, colors='black')
        ax.hlines(y=right_y, xmin=node.right.height, xmax=node.height, colors='black')
        
        # Draw vertical connector
        ax.vlines(x=node.height, ymin=left_y, ymax=right_y, colors='black')
        
        return (left_y + right_y) / 2
    
    # Calculate scaling parameters
    max_height = tree_root.height
    num_leaves = len([n for n in tree_root.get_leaves()])
    y_step = 1.0 / num_leaves
    
    # Plot the tree
    _plot_node(tree_root, 0, y_step)
    
    # Format the plot
    ax.set_xlabel('Needleman-Wunsch Similarity Score', fontsize=12)
    ax.set_title(f'Phylogenetic Tree (BLOSUM{blosum_type})', fontsize=14)
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # Save to file
    output_path = Path(output_dir) / f"phylogenetic_tree_blosum{blosum_type}.png"
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()