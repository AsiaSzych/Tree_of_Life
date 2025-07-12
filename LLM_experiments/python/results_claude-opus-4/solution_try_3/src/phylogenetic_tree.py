# Filename: src/phylogenetic_tree.py
"""Phylogenetic tree construction using single-linkage clustering."""

import logging
from typing import Dict, List, Tuple, Optional, Set
from pathlib import Path

from .tree_node import TreeNode
from .sequence_aligner import SequenceAligner

logger = logging.getLogger(__name__)


class PhylogeneticTree:
    """
    Builds phylogenetic tree using single-linkage clustering with similarity scores.
    """
    
    def __init__(self, scores: Dict[Tuple[str, str], int], blosum_type: int = 62):
        """
        Initialize with pairwise similarity scores.
        
        Args:
            scores: Dictionary mapping species pairs to Needleman-Wunsch scores
            blosum_type: BLOSUM matrix type used (50 or 62)
        """
        self.scores = scores
        self.blosum_type = blosum_type
        self.root: Optional[TreeNode] = None
        self.nodes: Dict[str, TreeNode] = {}
        self._cluster_id_counter = 0
    
    def _get_all_species(self) -> Set[str]:
        """Extract all unique species names from score pairs."""
        species = set()
        for (sp1, sp2) in self.scores.keys():
            species.add(sp1)
            species.add(sp2)
        return species
    
    def _get_similarity(self, cluster1: Set[str], cluster2: Set[str]) -> int:
        """
        Get similarity between two clusters using single linkage.
        
        Single linkage uses the maximum similarity between any pair of species
        from the two clusters.
        
        Args:
            cluster1: Set of species names in first cluster
            cluster2: Set of species names in second cluster
            
        Returns:
            Maximum similarity score between clusters
        """
        max_similarity = float('-inf')
        
        for sp1 in cluster1:
            for sp2 in cluster2:
                # Order the pair consistently
                if sp1 < sp2:
                    pair = (sp1, sp2)
                else:
                    pair = (sp2, sp1)
                
                if pair in self.scores:
                    max_similarity = max(max_similarity, self.scores[pair])
        
        return max_similarity
    
    def _generate_cluster_name(self) -> str:
        """Generate unique name for internal node."""
        self._cluster_id_counter += 1
        return f"ancestor_{self._cluster_id_counter}"
    
    def build_tree(self) -> TreeNode:
        """
        Build phylogenetic tree using agglomerative clustering.
        
        Returns:
            Root node of the constructed tree
        """
        # Initialize each species as a leaf node
        species_list = list(self._get_all_species())
        logger.info(f"Building tree for {len(species_list)} species")
        
        # Create leaf nodes
        active_clusters: Dict[str, TreeNode] = {}
        for species in species_list:
            node = TreeNode(name=species, height=0.0)
            self.nodes[species] = node
            active_clusters[species] = node
        
        # Track which species belong to each cluster
        cluster_members: Dict[str, Set[str]] = {
            name: {name} for name in species_list
        }
        
        # Iteratively merge clusters
        merge_count = 0
        while len(active_clusters) > 1:
            # Find pair of clusters with highest similarity
            best_similarity = float('-inf')
            best_pair = None
            
            cluster_names = list(active_clusters.keys())
            for i in range(len(cluster_names)):
                for j in range(i + 1, len(cluster_names)):
                    cluster1 = cluster_names[i]
                    cluster2 = cluster_names[j]
                    
                    similarity = self._get_similarity(
                        cluster_members[cluster1],
                        cluster_members[cluster2]
                    )
                    
                    if similarity > best_similarity:
                        best_similarity = similarity
                        best_pair = (cluster1, cluster2)
            
            if best_pair is None:
                raise ValueError("No valid pairs found for merging")
            
            # Merge the best pair
            cluster1, cluster2 = best_pair
            merge_count += 1
            
            logger.debug(
                f"Merge {merge_count}: {cluster1} + {cluster2} "
                f"at similarity {best_similarity}"
            )
            
            # Create new internal node
            new_cluster_name = self._generate_cluster_name()
            new_node = TreeNode(
                name=new_cluster_name,
                height=float(best_similarity),
                left=active_clusters[cluster1],
                right=active_clusters[cluster2]
            )
            
            # Update data structures
            self.nodes[new_cluster_name] = new_node
            active_clusters[new_cluster_name] = new_node
            
            # Combine cluster members
            cluster_members[new_cluster_name] = (
                cluster_members[cluster1] | cluster_members[cluster2]
            )
            
            # Remove merged clusters
            del active_clusters[cluster1]
            del active_clusters[cluster2]
            del cluster_members[cluster1]
            del cluster_members[cluster2]
        
        # Set root to the last remaining cluster
        self.root = list(active_clusters.values())[0]
        logger.info(f"Tree construction complete with {merge_count} merges")
        
        return self.root
    
    def get_clusters_at_threshold(self, threshold: float) -> List[Set[str]]:
        """
        Get clusters by cutting tree at given similarity threshold.
        
        Args:
            threshold: Similarity threshold for clustering
            
        Returns:
            List of clusters, each cluster is a set of species names
        """
        if not self.root:
            raise RuntimeError("Tree not built yet. Call build_tree() first.")
        
        def get_clusters_recursive(node: TreeNode) -> List[Set[str]]:
            # If this node's height is below threshold, return all leaves as one cluster
            if node.height <= threshold:
                return [node.get_leaf_names()]
            
            # If leaf node above threshold, it's its own cluster
            if node.is_leaf():
                return [{node.name}]
            
            # Otherwise, recursively get clusters from children
            clusters = []
            if node.left:
                clusters.extend(get_clusters_recursive(node.left))
            if node.right:
                clusters.extend(get_clusters_recursive(node.right))
            
            return clusters
        
        clusters = get_clusters_recursive(self.root)
        logger.info(f"Found {len(clusters)} clusters at threshold {threshold}")
        
        return clusters
    
    def save_newick_simple(self, filepath: Optional[Path] = None) -> Path:
        """
        Save tree in simple Newick format (no branch lengths).
        
        Args:
            filepath: Optional custom filepath. If not provided, uses default naming.
            
        Returns:
            Path to saved file
        """
        if not self.root:
            raise RuntimeError("Tree not built yet. Call build_tree() first.")
        
        if filepath is None:
            filepath = Path(f"tree_blosum{self.blosum_type}_newick.nw")
        
        newick_str = self.root.to_newick_simple() + ";"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(newick_str)
        
        logger.info(f"Saved simple Newick format to {filepath}")
        return filepath
    
    def save_newick_with_distances(self, filepath: Optional[Path] = None) -> Path:
        """
        Save tree in Newick format with integer branch lengths.
        
        Args:
            filepath: Optional custom filepath. If not provided, uses default naming.
            
        Returns:
            Path to saved file
        """
        if not self.root:
            raise RuntimeError("Tree not built yet. Call build_tree() first.")
        
        if filepath is None:
            filepath = Path(f"tree_blosum{self.blosum_type}_newick_with_distance.nw")
        
        newick_str = self.root.to_newick_with_distances() + ";"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(newick_str)
        
        logger.info(f"Saved Newick format with distances to {filepath}")
        return filepath
    
    def save_both_formats(self) -> Tuple[Path, Path]:
        """
        Save tree in both Newick formats.
        
        Returns:
            Tuple of (simple_filepath, distances_filepath)
        """
        simple_path = self.save_newick_simple()
        distances_path = self.save_newick_with_distances()
        return simple_path, distances_path


def build_tree_from_scores(
    scores_file: str = "organisms_scores_blosum62.json",
    blosum_type: int = 62,
    base_path: Path = Path(".")
) -> PhylogeneticTree:
    """
    Convenience function to build tree from saved scores file.
    
    Args:
        scores_file: Name of the JSON file with similarity scores
        blosum_type: BLOSUM matrix type (50 or 62)
        base_path: Base directory path
        
    Returns:
        PhylogeneticTree object with built tree
    """
    # Load scores
    aligner = SequenceAligner(base_path=base_path)
    scores = aligner.load_scores(scores_file)
    
    # Build tree
    tree = PhylogeneticTree(scores, blosum_type=blosum_type)
    tree.build_tree()
    
    return tree