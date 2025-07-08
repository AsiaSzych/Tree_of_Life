"""
Module for creating dendrogram visualizations of phylogenetic trees.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import numpy as np

from src.tree.phylogenetic_tree import PhylogeneticTree, TreeNode


class DendrogramDrawer:
    """Class for drawing horizontal dendrograms from phylogenetic trees."""
    
    def __init__(self, tree: PhylogeneticTree):
        """
        Initialize the dendrogram drawer.
        
        Args:
            tree: PhylogeneticTree object to visualize
        """
        self.tree = tree
        self.leaf_positions = {}
        self.node_positions = {}
        self.y_position = 0
        self.max_similarity = 0
        
    def _assign_leaf_positions(self, node: TreeNode) -> List[str]:
        """
        Assign y-positions to leaf nodes (species) in order.
        
        Args:
            node: Current tree node
            
        Returns:
            List of leaf names under this node
        """
        if node.is_leaf:
            self.leaf_positions[node.name] = self.y_position
            self.y_position += 1
            return [node.name]
        
        leaves = []
        if node.left:
            leaves.extend(self._assign_leaf_positions(node.left))
        if node.right:
            leaves.extend(self._assign_leaf_positions(node.right))
        
        return leaves
    
    def _calculate_node_positions(self, node: TreeNode) -> Tuple[float, float]:
        """
        Calculate x,y positions for each node.
        
        Args:
            node: Current tree node
            
        Returns:
            Tuple of (x_position, y_position) for this node
        """
        # X position is based on similarity score (height)
        x_pos = node.height
        
        if node.is_leaf:
            y_pos = self.leaf_positions[node.name]
        else:
            # Y position is the mean of children's y positions
            left_x, left_y = self._calculate_node_positions(node.left)
            right_x, right_y = self._calculate_node_positions(node.right)
            y_pos = (left_y + right_y) / 2
            
            # Store child positions for line drawing
            self.node_positions[node.left.name] = (left_x, left_y)
            self.node_positions[node.right.name] = (right_x, right_y)
        
        self.node_positions[node.name] = (x_pos, y_pos)
        return x_pos, y_pos
    
    def draw(self, figsize: Tuple[int, int] = (12, 8), 
             title: Optional[str] = None) -> plt.Figure:
        """
        Draw the dendrogram.
        
        Args:
            figsize: Figure size (width, height)
            title: Title for the dendrogram
            
        Returns:
            Matplotlib figure object
        """
        if not self.tree.root:
            raise ValueError("Tree has no root node")
        
        # Reset positions
        self.leaf_positions = {}
        self.node_positions = {}
        self.y_position = 0
        
        # Assign leaf positions
        self._assign_leaf_positions(self.tree.root)
        
        # Calculate all node positions
        self._calculate_node_positions(self.tree.root)
        
        # Find maximum similarity for x-axis scaling
        self.max_similarity = max(pos[0] for pos in self.node_positions.values())
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Draw the tree
        self._draw_node(ax, self.tree.root)
        
        # Add leaf labels
        for leaf_name, y_pos in self.leaf_positions.items():
            ax.text(self.max_similarity * 1.02, y_pos, leaf_name, 
                   va='center', fontsize=10)
        
        # Set axis properties
        ax.set_xlim(-self.max_similarity * 0.05, self.max_similarity * 1.15)
        ax.set_ylim(-0.5, len(self.leaf_positions) - 0.5)
        ax.set_xlabel('Needleman-Wunsch Similarity Score', fontsize=12)
        ax.set_ylabel('Species', fontsize=12)
        
        # Remove y-axis ticks
        ax.set_yticks([])
        
        # Add grid for better readability
        ax.grid(True, axis='x', alpha=0.3)
        
        # Add title
        if title:
            ax.set_title(title, fontsize=14, fontweight='bold')
        
        # Invert x-axis so higher similarity is on the left
        ax.invert_xaxis()
        
        plt.tight_layout()
        return fig
    
    def _draw_node(self, ax: plt.Axes, node: TreeNode):
        """
        Recursively draw nodes and branches.
        
        Args:
            ax: Matplotlib axes object
            node: Current tree node
        """
        if node.is_leaf:
            # Draw horizontal line from leaf to its position
            x_pos, y_pos = self.node_positions[node.name]
            ax.plot([x_pos, self.max_similarity], [y_pos, y_pos], 
                   'k-', linewidth=1)
        else:
            # Get positions
            node_x, node_y = self.node_positions[node.name]
            left_x, left_y = self.node_positions[node.left.name]
            right_x, right_y = self.node_positions[node.right.name]
            
            # Draw horizontal lines from children to merge point
            ax.plot([left_x, node_x], [left_y, left_y], 'k-', linewidth=1.5)
            ax.plot([right_x, node_x], [right_y, right_y], 'k-', linewidth=1.5)
            
            # Draw vertical line connecting children
            ax.plot([node_x, node_x], [left_y, right_y], 'k-', linewidth=1.5)
            
            # Add merge point marker
            ax.plot(node_x, node_y, 'ko', markersize=4)
            
            # Recursively draw children
            self._draw_node(ax, node.left)
            self._draw_node(ax, node.right)


def draw_dendrogram(tree: PhylogeneticTree, 
                   figsize: Tuple[int, int] = (12, 8),
                   title: Optional[str] = None) -> plt.Figure:
    """
    Draw a horizontal dendrogram from a phylogenetic tree.
    
    Args:
        tree: PhylogeneticTree object
        figsize: Figure size (width, height)
        title: Title for the dendrogram
        
    Returns:
        Matplotlib figure object
    """
    drawer = DendrogramDrawer(tree)
    return drawer.draw(figsize, title)


def save_dendrogram(tree: PhylogeneticTree, 
                   blosum_version: str,
                   output_dir: str = ".",
                   figsize: Tuple[int, int] = (12, 8),
                   dpi: int = 300) -> str:
    """
    Save dendrogram to PNG file.
    
    Args:
        tree: PhylogeneticTree object
        blosum_version: BLOSUM version used (e.g., "blosum50", "blosum62")
        output_dir: Directory to save output file
        figsize: Figure size (width, height)
        dpi: Resolution for saved image
        
    Returns:
        Path to saved file
    """
    # Create output directory if needed
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Generate filename
    filename = output_path / f"phylogenetic_tree_{blosum_version}.png"
    
    # Create dendrogram
    title = f"Phylogenetic Tree ({blosum_version.upper()})"
    fig = draw_dendrogram(tree, figsize, title)
    
    # Save to file
    fig.savefig(filename, dpi=dpi, bbox_inches='tight')
    plt.close(fig)
    
    print(f"Saved dendrogram to: {filename}")
    return str(filename)