"""Implements similarity-based hierarchical clustering for phylogenetic tree."""

from typing import Dict, List, Tuple, Optional
import numpy as np

class TreeNode:
    """Node in phylogenetic tree."""
    
    def __init__(self, 
                 name: str, 
                 height: int = 0, 
                 left: Optional['TreeNode'] = None,
                 right: Optional['TreeNode'] = None):
        self.name = name
        self.height = height  # NW score at merge point
        self.left = left
        self.right = right
    
    def is_leaf(self) -> bool:
        return self.left is None and self.right is None

def build_phylogenetic_tree(
    species: List[str],
    similarity_scores: Dict[Tuple[str, str], int]
) -> TreeNode:
    """Build phylogenetic tree using single-linkage clustering on similarity scores.
    
    Args:
        species: List of species names
        similarity_scores: Dict of pairwise NW scores
        
    Returns:
        Root node of the phylogenetic tree
    """
    # Initialize clusters - each species starts as its own cluster
    clusters = {s: TreeNode(s) for s in species}
    cluster_members = {s: {s} for s in species}  # Track members for single-linkage
    
    while len(clusters) > 1:
        # Find the two most similar clusters
        max_sim = -np.inf
        best_pair = None
        
        # Compare all pairs of current clusters
        cluster_list = list(clusters.keys())
        for i in range(len(cluster_list)):
            for j in range(i+1, len(cluster_list)):
                c1, c2 = cluster_list[i], cluster_list[j]
                
                # Single linkage: max similarity between any pair of members
                current_max = max(
                    similarity_scores.get((a, b), similarity_scores.get((b, a), -np.inf))
                    for a in cluster_members[c1]
                    for b in cluster_members[c2]
                )
                
                if current_max > max_sim:
                    max_sim = current_max
                    best_pair = (c1, c2)
        
        if not best_pair:
            raise ValueError("No valid pair found for merging")
        
        c1, c2 = best_pair
        
        # Create new internal node
        new_name = f"({clusters[c1].name}:{clusters[c2].name})"
        new_node = TreeNode(
            name=new_name,
            height=max_sim,
            left=clusters[c1],
            right=clusters[c2]
        )
        
        # Update cluster tracking
        new_members = cluster_members[c1].union(cluster_members[c2])
        del clusters[c1]
        del clusters[c2]
        del cluster_members[c1]
        del cluster_members[c2]
        
        clusters[new_name] = new_node
        cluster_members[new_name] = new_members
    
    return clusters.popitem()[1]  # Return root node