"""
Module for visualizing phylogenetic trees as dendrograms.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import LineCollection
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging

from .tree_structures import TreeNode, PhylogeneticTree


class DendrogramVisualizer:
    """Creates dendrogram visualizations of phylogenetic trees."""
    
    def __init__(self):
        """Initialize the dendrogram visualizer."""
        self.logger = logging.getLogger(__name__)
        self.node_positions = {}
        self.y_counter = 0
        
    def draw_dendrogram(self, tree: PhylogeneticTree, blosum_type: int, 
                       figsize: Tuple[int, int] = (12, 8)) -> str:
        """
        Draw a horizontal dendrogram and save to PNG file.
        
        Args:
            tree: PhylogeneticTree to visualize
            blosum_type: BLOSUM matrix type (50 or 62)
            figsize: Figure size as (width, height)
            
        Returns:
            Path to saved PNG file
        """
        if not tree.root:
            raise ValueError("Cannot draw dendrogram for empty tree")
        
        # Reset state
        self.node_positions = {}
        self.y_counter = 0
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Calculate node positions
        self._calculate_positions(tree.root)
        
        # Draw the tree
        self._draw_tree(tree.root, ax)
        
        # Customize plot
        self._customize_plot(ax, tree)
        
        # Save to file
        filename = f"phylogenetic_tree_blosum{blosum_type}.png"
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        self.logger.info(f"Saved dendrogram to {filename}")
        return filename
    
    def _calculate_positions(self, node: TreeNode) -> Tuple[float, float]:
        """
        Calculate x,y positions for each node in the tree.
        X position is based on height (similarity score).
        Y position is based on leaf ordering.
        """
        if node.is_leaf():
            # Leaf node: assign next available y position
            x = node.height
            y = self.y_counter
            self.y_counter += 1
            self.node_positions[node] = (x, y)
            return x, y
        
        # Internal node: position based on children
        child_positions = []
        for child in node.children:
            child_pos = self._calculate_positions(child)
            child_positions.append(child_pos)
        
        # X position is the node's height (similarity score)
        x = node.height
        
        # Y position is the mean of children's y positions
        y = np.mean([pos[1] for pos in child_positions])
        
        self.node_positions[node] = (x, y)
        return x, y
    
    def _draw_tree(self, node: TreeNode, ax: plt.Axes):
        """Recursively draw the tree structure."""
        if node.is_leaf():
            # Draw leaf label
            x, y = self.node_positions[node]
            ax.text(x - 5, y, node.name, ha='right', va='center', fontsize=10)
            return
        
        # Get node position
        node_x, node_y = self.node_positions[node]
        
        # Draw connections to children
        for child in node.children:
            child_x, child_y = self.node_positions[child]
            
            # Draw horizontal line from child to node's x position
            ax.plot([child_x, node_x], [child_y, child_y], 'k-', linewidth=1.5)
            
            # Draw vertical connector if needed
            if abs(node_y - child_y) > 0.01:  # Avoid drawing tiny vertical lines
                ax.plot([node_x, node_x], [child_y, node_y], 'k-', linewidth=1.5)
            
            # Recursively draw child
            self._draw_tree(child, ax)
    
    def _customize_plot(self, ax: plt.Axes, tree: PhylogeneticTree):
        """Customize the plot appearance."""
        # Set labels
        ax.set_xlabel('Needleman-Wunsch Similarity Score', fontsize=12)
        ax.set_ylabel('Species', fontsize=12)
        ax.set_title('Phylogenetic Tree Dendrogram', fontsize=14, fontweight='bold')
        
        # Remove y-axis ticks (species names are drawn as text)
        ax.set_yticks([])
        
        # Set x-axis to show similarity scores
        ax.invert_xaxis()  # Higher similarity (more recent divergence) on the left
        
        # Add grid for x-axis
        ax.grid(True, axis='x', alpha=0.3, linestyle='--')
        
        # Set axis limits with some padding
        all_x = [pos[0] for pos in self.node_positions.values()]
        all_y = [pos[1] for pos in self.node_positions.values()]
        
        x_margin = (max(all_x) - min(all_x)) * 0.1
        y_margin = 0.5
        
        ax.set_xlim(max(all_x) + x_margin, min(all_x) - x_margin * 5)  # Extra space for labels
        ax.set_ylim(min(all_y) - y_margin, max(all_y) + y_margin)
        
        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Add a note about the scale
        ax.text(0.02, 0.98, f'Branch lengths represent similarity scores', 
                transform=ax.transAxes, fontsize=9, va='top', 
                bbox=dict(boxstyle='round,pad=0.3', facecolor='wheat', alpha=0.5))


class EnhancedDendrogramVisualizer(DendrogramVisualizer):
    """Enhanced dendrogram visualizer with additional features."""
    
    def draw_dendrogram_with_clusters(self, tree: PhylogeneticTree, blosum_type: int,
                                    threshold: Optional[float] = None,
                                    figsize: Tuple[int, int] = (12, 8)) -> str:
        """
        Draw dendrogram with optional cluster threshold line.
        
        Args:
            tree: PhylogeneticTree to visualize
            blosum_type: BLOSUM matrix type (50 or 62)
            threshold: Optional similarity threshold to show cluster cutoff
            figsize: Figure size as (width, height)
            
        Returns:
            Path to saved PNG file
        """
        if not tree.root:
            raise ValueError("Cannot draw dendrogram for empty tree")
        
        # Reset state
        self.node_positions = {}
        self.y_counter = 0
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Calculate node positions
        self._calculate_positions(tree.root)
        
        # Draw the tree with colors if threshold is provided
        if threshold:
            clusters = tree.get_clusters_at_threshold(threshold)
            self._draw_tree_with_clusters(tree.root, ax, threshold, clusters)
        else:
            self._draw_tree(tree.root, ax)
        
        # Draw threshold line if provided
        if threshold:
            ax.axvline(x=threshold, color='red', linestyle='--', linewidth=2, 
                      label=f'Threshold: {threshold}')
            ax.legend()
        
        # Customize plot
        self._customize_plot(ax, tree)
        
        # Save to file
        if threshold:
            filename = f"phylogenetic_tree_blosum{blosum_type}_threshold_{int(threshold)}.png"
        else:
            filename = f"phylogenetic_tree_blosum{blosum_type}.png"
            
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        self.logger.info(f"Saved dendrogram to {filename}")
        return filename
    
    def _draw_tree_with_clusters(self, node: TreeNode, ax: plt.Axes, 
                               threshold: float, clusters: List[List[str]]):
        """Draw tree with different colors for different clusters."""
        # Create color map for clusters
        colors = plt.cm.Set3(np.linspace(0, 1, len(clusters)))
        cluster_colors = {}
        
        for i, cluster in enumerate(clusters):
            for species in cluster:
                cluster_colors[species] = colors[i]
        
        self._draw_colored_tree(node, ax, cluster_colors, threshold)
    
    def _draw_colored_tree(self, node: TreeNode, ax: plt.Axes, 
                         cluster_colors: Dict[str, np.ndarray], threshold: float):
        """Draw tree with colored branches based on clusters."""
        if node.is_leaf():
            # Draw leaf label with cluster color
            x, y = self.node_positions[node]
            color = cluster_colors.get(node.name, 'black')
            ax.text(x - 5, y, node.name, ha='right', va='center', 
                   fontsize=10, color=color, weight='bold')
            return
        
        # Get node position
        node_x, node_y = self.node_positions[node]
        
        # Determine line color based on threshold
        line_color = 'gray' if node.height >= threshold else 'black'
        line_width = 1.0 if node.height >= threshold else 1.5
        
        # Draw connections to children
        for child in node.children:
            child_x, child_y = self.node_positions[child]
            
            # Draw horizontal line
            ax.plot([child_x, node_x], [child_y, child_y], 
                   color=line_color, linewidth=line_width)
            
            # Draw vertical connector
            if abs(node_y - child_y) > 0.01:
                ax.plot([node_x, node_x], [child_y, node_y], 
                       color=line_color, linewidth=line_width)
            
            # Recursively draw child
            self._draw_colored_tree(child, ax, cluster_colors, threshold)