"""
Module for analyzing clusters at different similarity thresholds.
"""
import json
import logging
from pathlib import Path
from typing import List, Dict

from .tree_structures import PhylogeneticTree
from .tree_builder import SingleLinkageTreeBuilder
from .score_saver import ScoreSaver


class ClusterAnalyzer:
    """Analyzes phylogenetic tree clusters at various thresholds."""
    
    def __init__(self, blosum_type: int = 62):
        """
        Initialize the cluster analyzer.
        
        Args:
            blosum_type: BLOSUM matrix type (50 or 62)
        """
        self.blosum_type = blosum_type
        self.logger = logging.getLogger(__name__)
        self.tree_builder = SingleLinkageTreeBuilder()
    
    def load_thresholds(self, filepath: str = "thresholds.txt") -> List[int]:
        """
        Load threshold values from text file.
        
        Args:
            filepath: Path to thresholds file
            
        Returns:
            List of threshold values as integers
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Thresholds file not found: {filepath}")
        
        thresholds = []
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:  # Skip empty lines
                    try:
                        threshold = int(line)
                        thresholds.append(threshold)
                    except ValueError:
                        self.logger.warning(f"Skipping invalid threshold value: {line}")
        
        self.logger.info(f"Loaded {len(thresholds)} thresholds from {filepath}")
        return sorted(thresholds, reverse=True)  # Sort from highest to lowest
    
    def analyze_clusters(self, tree: PhylogeneticTree, thresholds: List[int] = None) -> Dict[int, List[List[str]]]:
        """
        Analyze clusters at multiple thresholds.
        
        Args:
            tree: PhylogeneticTree to analyze
            thresholds: List of threshold values (if None, loads from file)
            
        Returns:
            Dictionary mapping thresholds to cluster lists
        """
        if thresholds is None:
            thresholds = self.load_thresholds()
        
        results = {}
        
        for threshold in thresholds:
            self.logger.info(f"Calculating clusters for threshold: {threshold}")
            
            # Get clusters at this threshold
            clusters = tree.get_clusters_at_threshold(float(threshold))
            
            # Sort clusters by size (largest first) and then alphabetically
            clusters = sorted(clusters, key=lambda c: (-len(c), sorted(c)[0]))
            
            # Sort species within each cluster alphabetically
            clusters = [sorted(cluster) for cluster in clusters]
            
            results[threshold] = clusters
            
            self.logger.info(f"  Found {len(clusters)} clusters")
            for i, cluster in enumerate(clusters):
                self.logger.debug(f"    Cluster {i+1}: {len(cluster)} species")
        
        return results
    
    def save_clusters(self, clusters: Dict[int, List[List[str]]]) -> str:
        """
        Save cluster results to JSON file.
        
        Args:
            clusters: Dictionary mapping thresholds to cluster lists
            
        Returns:
            Path to saved file
        """
        filename = f"clusters_for_blosum{self.blosum_type}.json"
        path = Path(filename)
        
        try:
            with open(path, 'w') as f:
                json.dump(clusters, f, indent=2)
            
            self.logger.info(f"Saved cluster results to {filename}")
            return str(path)
            
        except Exception as e:
            self.logger.error(f"Error saving clusters: {e}")
            raise
    
    def print_clusters(self, clusters: Dict[int, List[List[str]]]):
        """
        Print cluster results to standard output.
        
        Args:
            clusters: Dictionary mapping thresholds to cluster lists
        """
        print("\n" + "="*60)
        print(f"CLUSTER ANALYSIS RESULTS (BLOSUM{self.blosum_type})")
        print("="*60)
        
        for threshold in sorted(clusters.keys(), reverse=True):
            cluster_list = clusters[threshold]
            print(f"\nThreshold: {threshold}")
            print(f"Number of clusters: {len(cluster_list)}")
            print("-" * 40)
            
            for i, cluster in enumerate(cluster_list, 1):
                print(f"Cluster {i} ({len(cluster)} species):")
                # Print species in a formatted way
                if len(cluster) <= 5:
                    print(f"  {', '.join(cluster)}")
                else:
                    # For large clusters, show first few and count
                    shown = ', '.join(cluster[:3])
                    print(f"  {shown}, ... and {len(cluster)-3} more")
            
            # Summary statistics
            sizes = [len(c) for c in cluster_list]
            if sizes:
                print(f"\nCluster size statistics:")
                print(f"  Min size: {min(sizes)}")
                print(f"  Max size: {max(sizes)}")
                print(f"  Average size: {sum(sizes)/len(sizes):.1f}")
    
    def run_full_analysis(self, tree: PhylogeneticTree = None) -> Dict[int, List[List[str]]]:
        """
        Run complete cluster analysis pipeline.
        
        Args:
            tree: Pre-built tree (if None, builds from saved scores)
            
        Returns:
            Dictionary mapping thresholds to cluster lists
        """
        # Build tree if not provided
        if tree is None:
            self.logger.info("Building tree from saved scores")
            tree = self.tree_builder.build_from_file(self.blosum_type)
        
        # Load thresholds and analyze
        thresholds = self.load_thresholds()
        clusters = self.analyze_clusters(tree, thresholds)
        
        # Print results
        self.print_clusters(clusters)
        
        # Save to file
        self.save_clusters(clusters)
        
        return clusters