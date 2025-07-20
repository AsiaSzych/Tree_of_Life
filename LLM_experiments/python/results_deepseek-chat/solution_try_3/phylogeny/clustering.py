"""Threshold-based clustering of phylogenetic trees."""

from typing import List, Dict, Set
from .tree import TreeNode

def get_clusters_at_threshold(tree: TreeNode, threshold: int) -> List[List[str]]:
    """Extract clusters of leaf nodes at a given similarity threshold.
    
    Args:
        tree: Root node of the phylogenetic tree
        threshold: Minimum similarity score for nodes to remain connected
        
    Returns:
        List of clusters, each containing species names
    """
    clusters = []
    
    def _traverse(node: TreeNode) -> Set[str]:
        if node.is_leaf():
            return {node.name}
        
        left_cluster = _traverse(node.left)
        right_cluster = _traverse(node.right)
        
        # Merge if the node's height (NW score) >= threshold
        if node.height >= threshold:
            return left_cluster.union(right_cluster)
        else:
            if left_cluster:
                clusters.append(sorted(list(left_cluster)))
            if right_cluster:
                clusters.append(sorted(list(right_cluster)))
            return set()
    
    final_cluster = _traverse(tree)
    if final_cluster:
        clusters.append(sorted(list(final_cluster)))
    
    # Remove duplicates and empty clusters
    unique_clusters = []
    seen = set()
    for cluster in clusters:
        if cluster and tuple(cluster) not in seen:
            seen.add(tuple(cluster))
            unique_clusters.append(cluster)
    
    return unique_clusters

def load_thresholds(file_path: str) -> List[int]:
    """Load thresholds from file.
    
    Args:
        file_path: Path to thresholds.txt
        
    Returns:
        List of integer thresholds
    """
    with open(file_path, 'r') as f:
        return [int(line.strip()) for line in f if line.strip()]