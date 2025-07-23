"""
Module for saving phylogenetic trees in various formats.
"""
import logging
from pathlib import Path
from typing import Optional, Tuple

from .tree_structures import PhylogeneticTree


class TreeSaver:
    """Handles saving phylogenetic trees to various file formats."""
    
    def __init__(self):
        """Initialize the tree saver."""
        self.logger = logging.getLogger(__name__)
    
    def save_newick_formats(self, tree: PhylogeneticTree, blosum_type: int) -> Tuple[str, str]:
        """
        Save tree in both Newick format variants.
        
        Args:
            tree: PhylogeneticTree object to save
            blosum_type: BLOSUM matrix type (50 or 62)
            
        Returns:
            Tuple of (simple_newick_path, distance_newick_path)
        """
        # Save simple Newick (names only)
        simple_path = self._save_simple_newick(tree, blosum_type)
        
        # Save Newick with distances
        distance_path = self._save_newick_with_distances(tree, blosum_type)
        
        return simple_path, distance_path
    
    def _save_simple_newick(self, tree: PhylogeneticTree, blosum_type: int) -> str:
        """Save tree in simple Newick format (names only)."""
        filename = f"tree_blosum{blosum_type}_newick.nw"
        path = Path(filename)
        
        try:
            newick_string = tree.get_newick_simple()
            
            with open(path, 'w') as f:
                f.write(newick_string)
            
            self.logger.info(f"Saved simple Newick format to {filename}")
            return str(path)
            
        except Exception as e:
            self.logger.error(f"Error saving simple Newick format: {e}")
            raise
    
    def _save_newick_with_distances(self, tree: PhylogeneticTree, blosum_type: int) -> str:
        """Save tree in Newick format with branch distances."""
        filename = f"tree_blosum{blosum_type}_newick_with_distance.nw"
        path = Path(filename)
        
        try:
            newick_string = tree.get_newick_with_distances()
            
            with open(path, 'w') as f:
                f.write(newick_string)
            
            self.logger.info(f"Saved Newick with distances to {filename}")
            return str(path)
            
        except Exception as e:
            self.logger.error(f"Error saving Newick with distances: {e}")
            raise
    
    @staticmethod
    def load_newick(filepath: str) -> str:
        """
        Load Newick string from file.
        
        Args:
            filepath: Path to Newick file
            
        Returns:
            Newick format string
        """
        path = Path(filepath)
        
        if not path.exists():
            raise FileNotFoundError(f"Newick file not found: {filepath}")
        
        with open(path, 'r') as f:
            return f.read().strip()