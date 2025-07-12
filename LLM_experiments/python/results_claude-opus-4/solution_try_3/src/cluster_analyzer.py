"""Analyze clusters at different similarity thresholds."""

import json
import logging
from pathlib import Path
from typing import List, Dict, Set

from .phylogenetic_tree import PhylogeneticTree, build_tree_from_scores

logger = logging.getLogger(__name__)


class ClusterAnalyzer:
    """Analyzes phylogenetic clusters at various thresholds."""
    
    def __init__(self, tree: PhylogeneticTree):
        """
        Initialize analyzer with a phylogenetic tree.
        
        Args:
            tree: PhylogeneticTree object with built tree
        """
        if not tree.root:
            raise ValueError("Tree must be built before analysis")
        
        self.tree = tree
        self.blosum_type = tree.blosum_type
    
    def load_thresholds(self, filepath: Path = Path("thresholds.txt")) -> List[int]:
        """
        Load threshold values from text file.
        
        Args:
            filepath: Path to thresholds file
            
        Returns:
            List of integer threshold values
            
        Raises:
            FileNotFoundError: If thresholds file doesn't exist
            ValueError: If file contains invalid values
        """
        if not filepath.exists():
            raise FileNotFoundError(f"Thresholds file not found: {filepath}")
        
        thresholds = []
        
        try:
            with open(filepath, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:  # Skip empty lines
                        continue
                    
                    try:
                        threshold = int(line)
                        thresholds.append(threshold)
                    except ValueError:
                        raise ValueError(
                            f"Invalid threshold value on line {line_num}: '{line}'"
                        )
            
            logger.info(f"Loaded {len(thresholds)} thresholds from {filepath}")
            return thresholds
            
        except IOError as e:
            logger.error(f"Error reading thresholds file: {e}")
            raise
    
    def analyze_clusters(self, thresholds: List[int]) -> Dict[int, List[List[str]]]:
        """
        Generate clusters for each threshold value.
        
        Args:
            thresholds: List of threshold values
            
        Returns:
            Dictionary mapping thresholds to cluster lists
        """
        results = {}
        
        for threshold in thresholds:
            # Get clusters as sets
            cluster_sets = self.tree.get_clusters_at_threshold(threshold)
            
            # Convert sets to sorted lists for consistent output
            cluster_lists = [sorted(list(cluster)) for cluster in cluster_sets]
            
            # Sort clusters by size (descending) then alphabetically by first element
            cluster_lists.sort(key=lambda x: (-len(x), x[0]))
            
            results[threshold] = cluster_lists
            
            logger.info(
                f"Threshold {threshold}: Found {len(cluster_lists)} clusters "
                f"with sizes {[len(c) for c in cluster_lists]}"
            )
        
        return results
    
    def print_clusters(self, clusters_dict: Dict[int, List[List[str]]]) -> None:
        """
        Print clusters to standard output in a readable format.
        
        Args:
            clusters_dict: Dictionary mapping thresholds to cluster lists
        """
        print(f"\n{'='*60}")
        print(f"Clustering Results (BLOSUM{self.blosum_type})")
        print(f"{'='*60}\n")
        
        for threshold in sorted(clusters_dict.keys()):
            clusters = clusters_dict[threshold]
            print(f"Threshold: {threshold}")
            print(f"Number of clusters: {len(clusters)}")
            
            for i, cluster in enumerate(clusters, 1):
                print(f"  Cluster {i} ({len(cluster)} species): {', '.join(cluster)}")
            
            print()  # Empty line between thresholds
    
    def save_clusters(self, 
                     clusters_dict: Dict[int, List[List[str]]], 
                     filepath: Path = None) -> Path:
        """
        Save clusters to JSON file.
        
        Args:
            clusters_dict: Dictionary mapping thresholds to cluster lists
            filepath: Optional custom filepath
            
        Returns:
            Path to saved file
        """
        if filepath is None:
            filepath = Path(f"clusters_for_blosum{self.blosum_type}.json")
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(clusters_dict, f, indent=2, sort_keys=True)
            
            logger.info(f"Saved clustering results to {filepath}")
            return filepath
            
        except IOError as e:
            logger.error(f"Error saving clusters: {e}")
            raise
    
    def run_analysis(self, 
                    thresholds_file: Path = Path("thresholds.txt"),
                    output_file: Path = None) -> Dict[int, List[List[str]]]:
        """
        Complete clustering analysis pipeline.
        
        Args:
            thresholds_file: Path to thresholds file
            output_file: Optional custom output filepath
            
        Returns:
            Dictionary mapping thresholds to cluster lists
        """
        # Load thresholds
        thresholds = self.load_thresholds(thresholds_file)
        
        # Generate clusters
        clusters_dict = self.analyze_clusters(thresholds)
        
        # Print results
        self.print_clusters(clusters_dict)
        
        # Save to file
        self.save_clusters(clusters_dict, output_file)
        
        return clusters_dict


def analyze_clusters_from_tree(
    tree: PhylogeneticTree,
    thresholds_file: Path = Path("thresholds.txt")
) -> Dict[int, List[List[str]]]:
    """
    Convenience function to run cluster analysis on a tree.
    
    Args:
        tree: Built phylogenetic tree
        thresholds_file: Path to thresholds file
        
    Returns:
        Dictionary mapping thresholds to cluster lists
    """
    analyzer = ClusterAnalyzer(tree)
    return analyzer.run_analysis(thresholds_file)


def analyze_clusters_from_scores(
    scores_file: str = "organisms_scores_blosum62.json",
    blosum_type: int = 62,
    thresholds_file: Path = Path("thresholds.txt"),
    base_path: Path = Path(".")
) -> Dict[int, List[List[str]]]:
    """
    Complete pipeline from scores to clusters.
    
    Args:
        scores_file: Name of the JSON file with similarity scores
        blosum_type: BLOSUM matrix type (50 or 62)
        thresholds_file: Path to thresholds file
        base_path: Base directory path
        
    Returns:
        Dictionary mapping thresholds to cluster lists
    """
    # Build tree
    tree = build_tree_from_scores(scores_file, blosum_type, base_path)
    
    # Analyze clusters
    return analyze_clusters_from_tree(tree, thresholds_file)