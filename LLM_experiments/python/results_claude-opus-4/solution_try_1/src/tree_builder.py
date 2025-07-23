"""
Module for building phylogenetic trees using single-linkage clustering.
"""
import logging
from typing import Dict, Tuple, List, Set
import numpy as np

from .tree_structures import TreeNode, PhylogeneticTree
from .score_saver import ScoreSaver


class SingleLinkageTreeBuilder:
    """Builds phylogenetic trees using single-linkage clustering with similarity scores."""
    
    def __init__(self):
        """Initialize the tree builder."""
        self.logger = logging.getLogger(__name__)
    
    def build_tree(self, scores: Dict[Tuple[str, str], int]) -> PhylogeneticTree:
        """
        Build a phylogenetic tree using single-linkage clustering.
        
        Args:
            scores: Dictionary mapping species pairs to similarity scores
            
        Returns:
            PhylogeneticTree object
        """
        # Extract unique species names
        species = set()
        for (sp1, sp2) in scores.keys():
            species.add(sp1)
            species.add(sp2)
        
        species_list = sorted(list(species))
        self.logger.info(f"Building tree for {len(species_list)} species")
        
        # Initialize clusters - each species starts as its own cluster
        clusters = {}
        for sp in species_list:
            node = TreeNode(name=sp, height=0.0)
            clusters[sp] = node
        
        # Track which species are in which cluster
        cluster_members = {sp: {sp} for sp in species_list}
        
        # Build tree by iteratively merging most similar clusters
        merge_count = 0
        while len(clusters) > 1:
            # Find the pair of clusters with highest similarity
            max_similarity = float('-inf')
            best_pair = None
            
            cluster_names = list(clusters.keys())
            for i in range(len(cluster_names)):
                for j in range(i + 1, len(cluster_names)):
                    cluster1 = cluster_names[i]
                    cluster2 = cluster_names[j]
                    
                    # Single linkage: find maximum similarity between any pair
                    similarity = self._get_cluster_similarity(
                        cluster_members[cluster1],
                        cluster_members[cluster2],
                        scores
                    )
                    
                    if similarity > max_similarity:
                        max_similarity = similarity
                        best_pair = (cluster1, cluster2)
            
            if best_pair is None:
                break
            
            # Merge the two most similar clusters
            cluster1_name, cluster2_name = best_pair
            merge_count += 1
            
            self.logger.debug(
                f"Merge {merge_count}: {cluster1_name} + {cluster2_name} "
                f"at similarity {max_similarity}"
            )
            
            # Create new internal node
            new_node = TreeNode(height=float(max_similarity))
            new_node.add_child(clusters[cluster1_name])
            new_node.add_child(clusters[cluster2_name])
            
            # Update clusters
            new_cluster_name = f"cluster_{merge_count}"
            clusters[new_cluster_name] = new_node
            
            # Update cluster members
            cluster_members[new_cluster_name] = (
                cluster_members[cluster1_name] | cluster_members[cluster2_name]
            )
            
            # Remove merged clusters
            del clusters[cluster1_name]
            del clusters[cluster2_name]
            del cluster_members[cluster1_name]
            del cluster_members[cluster2_name]
        
        # The last remaining cluster is the root
        root = list(clusters.values())[0] if clusters else None
        
        tree = PhylogeneticTree(root=root)
        self.logger.info(f"Tree construction complete with {merge_count} merges")
        
        return tree
    
    def _get_cluster_similarity(
        self, 
        members1: Set[str], 
        members2: Set[str], 
        scores: Dict[Tuple[str, str], int]
    ) -> int:
        """
        Calculate single-linkage similarity between two clusters.
        
        Returns the maximum similarity between any pair of species
        from the two clusters.
        """
        max_similarity = float('-inf')
        
        for sp1 in members1:
            for sp2 in members2:
                # Handle both orderings of the tuple key
                if (sp1, sp2) in scores:
                    similarity = scores[(sp1, sp2)]
                elif (sp2, sp1) in scores:
                    similarity = scores[(sp2, sp1)]
                else:
                    continue
                
                max_similarity = max(max_similarity, similarity)
        
        return max_similarity
    
    def build_from_file(self, blosum_type: int) -> PhylogeneticTree:
        """
        Build tree from saved similarity scores file.
        
        Args:
            blosum_type: BLOSUM matrix type (50 or 62)
            
        Returns:
            PhylogeneticTree object
        """
        # Load scores from file
        saved_scores = ScoreSaver.load_scores(blosum_type)
        
        # Convert back to tuple format
        scores = {}
        for key, value in saved_scores.items():
            species1, species2 = key.split('_', 1)
            scores[(species1, species2)] = value
        
        return self.build_tree(scores)