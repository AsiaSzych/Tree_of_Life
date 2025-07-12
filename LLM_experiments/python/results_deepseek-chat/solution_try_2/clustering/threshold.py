from pathlib import Path
from typing import List, Dict, Set
from tree.node import TreeNode
import json

def read_thresholds(file_path: str) -> List[int]:
    """Read thresholds from file and return as sorted list of integers."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Thresholds file not found: {file_path}")
    
    with open(path, 'r') as f:
        thresholds = [int(line.strip()) for line in f if line.strip()]
    
    return sorted(thresholds, reverse=True)

def get_clusters_at_threshold(root: TreeNode, threshold: int) -> List[List[str]]:
    """
    Extract clusters of leaf nodes at a given threshold.
    
    Args:
        root: Root node of the phylogenetic tree
        threshold: Minimum NW score to consider a merge
        
    Returns:
        List of clusters, where each cluster is a list of species names
    """
    def _traverse(node: TreeNode) -> List[Set[str]]:
        if node.is_leaf():
            return [{node.name}]
        
        left_clusters = _traverse(node.left)
        right_clusters = _traverse(node.right)
        
        if node.height >= threshold:
            # Merge all clusters from both branches
            merged = [cluster for clusters in [left_clusters, right_clusters] for cluster in clusters]
            return [set().union(*merged)] if len(merged) > 1 else merged
        else:
            # Keep clusters separate
            return left_clusters + right_clusters
    
    # Convert sets to sorted lists for consistent output
    cluster_sets = _traverse(root)
    return [sorted(cluster) for cluster in cluster_sets]

def save_clusters_to_json(clusters: Dict[int, List[List[str]]], 
                         blosum_type: str, 
                         output_dir: str = "./output") -> None:
    """Save clusters to JSON file in specified format."""
    Path(output_dir).mkdir(exist_ok=True)
    output_path = Path(output_dir) / f"clusters_for_blosum{blosum_type}.json"
    
    with open(output_path, 'w') as f:
        json.dump(clusters, f, indent=4)