"""Dendrogram visualization for phylogenetic trees."""

import logging
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from typing import Dict, List, Tuple, Optional
from pathlib import Path

from .tree_node import TreeNode
from .phylogenetic_tree import PhylogeneticTree

logger = logging.getLogger(__name__)


class DendrogramPlotter:
    """Creates dendrogram visualizations of phylogenetic trees."""
    
    def __init__(self, tree: PhylogeneticTree):
        """
        Initialize plotter with a phylogenetic tree.
        
        Args:
            tree: PhylogeneticTree object with built tree
        """
        if not tree.root:
            raise ValueError("Tree must be built before plotting")
        
        self.tree = tree
        self.root = tree.root
        self.leaf_positions: Dict[str, float] = {}
        self.node_positions: Dict[str, Tuple[float, float]] = {}
    
    def _assign_leaf_positions(self) -> List[str]:
        """
        Assign y-positions to leaf nodes.
        
        Returns:
            Ordered list of species names
        """
        leaves = self.root.get_leaves()
        species_names = sorted([leaf.name for leaf in leaves])
        
        # Assign evenly spaced positions
        for i, species in enumerate(species_names):
            self.leaf_positions[species] = i
        
        return species_names
    
    def _calculate_node_positions(self, node: TreeNode) -> Tuple[float, float]:
        """
        Calculate x,y position for each node.
        
        Args:
            node: Tree node to position
            
        Returns:
            Tuple of (x_position, y_position)
        """
        # X position is the similarity score (height)
        x_pos = node.height
        
        if node.is_leaf():
            # Y position for leaves
            y_pos = self.leaf_positions[node.name]
        else:
            # Y position for internal nodes is average of children
            left_x, left_y = self._calculate_node_positions(node.left)
            right_x, right_y = self._calculate_node_positions(node.right)
            y_pos = (left_y + right_y) / 2
        
        self.node_positions[node.name] = (x_pos, y_pos)
        return x_pos, y_pos
    
    def _draw_node(self, ax: plt.Axes, node: TreeNode) -> None:
        """
        Recursively draw node and its connections.
        
        Args:
            ax: Matplotlib axes to draw on
            node: Tree node to draw
        """
        if node.is_leaf():
            return
        
        # Get positions
        node_x, node_y = self.node_positions[node.name]
        
        # Draw connections to children
        if node.left:
            left_x, left_y = self.node_positions[node.left.name]
            # Horizontal line from child to merge point
            ax.plot([left_x, node_x], [left_y, left_y], 'k-', linewidth=1.5)
            # Vertical line at merge point
            ax.plot([node_x, node_x], [left_y, node_y], 'k-', linewidth=1.5)
            # Recursively draw left subtree
            self._draw_node(ax, node.left)
        
        if node.right:
            right_x, right_y = self.node_positions[node.right.name]
            # Horizontal line from child to merge point
            ax.plot([right_x, node_x], [right_y, right_y], 'k-', linewidth=1.5)
            # Vertical line at merge point
            ax.plot([node_x, node_x], [right_y, node_y], 'k-', linewidth=1.5)
            # Recursively draw right subtree
            self._draw_node(ax, node.right)
    
    def plot(self, 
             figsize: Tuple[float, float] = (12, 8),
             title: Optional[str] = None,
             save_path: Optional[Path] = None,
             dpi: int = 300) -> plt.Figure:
        """
        Create dendrogram plot.
        
        Args:
            figsize: Figure size in inches (width, height)
            title: Plot title
            save_path: Path to save the plot
            dpi: Resolution for saved image
            
        Returns:
            Matplotlib figure object
        """
        # Assign positions
        species_names = self._assign_leaf_positions()
        self._calculate_node_positions(self.root)
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Draw the tree
        self._draw_node(ax, self.root)
        
        # Draw leaf labels
        for species in species_names:
            y_pos = self.leaf_positions[species]
            ax.text(-5, y_pos, species, ha='right', va='center', fontsize=10)
        
        # Set axis properties
        ax.set_xlabel('Needleman-Wunsch Similarity Score', fontsize=12)
        ax.set_ylabel('Species', fontsize=12)
        
        # Set title
        if title:
            ax.set_title(title, fontsize=14, fontweight='bold')
        else:
            ax.set_title(
                f'Phylogenetic Tree (BLOSUM{self.tree.blosum_type})',
                fontsize=14,
                fontweight='bold'
            )
        
        # Adjust plot limits
        x_min = -50  # Leave space for labels
        x_max = self.root.height * 1.05  # Add 5% margin
        y_min = -0.5
        y_max = len(species_names) - 0.5
        
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        
        # Remove y-axis ticks
        ax.set_yticks([])
        
        # Add grid for x-axis
        ax.grid(True, axis='x', alpha=0.3)
        
        # Tight layout
        plt.tight_layout()
        
        # Save if path provided
        if save_path:
            fig.savefig(save_path, dpi=dpi, bbox_inches='tight')
            logger.info(f"Saved dendrogram to {save_path}")
        
        return fig
    
    def plot_with_threshold(self,
                          threshold: float,
                          figsize: Tuple[float, float] = (12, 8),
                          save_path: Optional[Path] = None,
                          dpi: int = 300) -> plt.Figure:
        """
        Create dendrogram with threshold line showing clusters.
        
        Args:
            threshold: Similarity threshold for clustering
            figsize: Figure size in inches
            save_path: Path to save the plot
            dpi: Resolution for saved image
            
        Returns:
            Matplotlib figure object
        """
        # Create base plot
        fig = self.plot(figsize=figsize, dpi=dpi)
        ax = fig.gca()
        
        # Add threshold line
        ax.axvline(x=threshold, color='red', linestyle='--', linewidth=2, 
                  label=f'Threshold: {threshold}')
        
        # Add legend
        ax.legend(loc='upper left')
        
        # Update title
        ax.set_title(
            f'Phylogenetic Tree (BLOSUM{self.tree.blosum_type}) - '
            f'Threshold: {threshold}',
            fontsize=14,
            fontweight='bold'
        )
        
        # Save if path provided
        if save_path:
            fig.savefig(save_path, dpi=dpi, bbox_inches='tight')
            logger.info(f"Saved dendrogram with threshold to {save_path}")
        
        return fig


def create_dendrogram(tree: PhylogeneticTree,
                     output_dir: Path = Path("."),
                     show_plot: bool = False) -> Path:
    """
    Convenience function to create and save dendrogram.
    
    Args:
        tree: PhylogeneticTree object with built tree
        output_dir: Directory to save the plot
        show_plot: Whether to display the plot
        
    Returns:
        Path to saved dendrogram
    """
    plotter = DendrogramPlotter(tree)
    
    # Create output filename
    filename = f"phylogenetic_tree_blosum{tree.blosum_type}.png"
    save_path = output_dir / filename
    
    # Create plot
    fig = plotter.plot(save_path=save_path)
    
    if show_plot:
        plt.show()
    else:
        plt.close(fig)
    
    return save_path