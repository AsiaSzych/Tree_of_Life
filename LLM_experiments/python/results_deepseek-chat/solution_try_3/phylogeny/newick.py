"""Handles Newick format tree export."""

from typing import Optional
from .tree import TreeNode

def to_simple_newick(node: TreeNode) -> str:
    """Convert tree to Newick format without distances.
    
    Args:
        node: Root node of the tree
        
    Returns:
        Newick format string without branch lengths
    """
    if node.is_leaf():
        return node.name
    
    left_str = to_simple_newick(node.left)
    right_str = to_simple_newick(node.right)
    return f"({left_str},{right_str})"

def to_distance_newick(node: TreeNode, parent_height: int = 0) -> str:
    """Convert tree to Newick format with integer distances.
    
    Args:
        node: Current node in the tree
        parent_height: Height of parent node for distance calculation
        
    Returns:
        Newick format string with integer branch lengths
    """
    if node.is_leaf():
        distance = parent_height - node.height
        return f"{node.name}:{max(distance, 0)}"  # Ensure non-negative
    
    left_str = to_distance_newick(node.left, node.height)
    right_str = to_distance_newick(node.right, node.height)
    
    if parent_height > 0:  # Not root node
        distance = parent_height - node.height
        return f"({left_str},{right_str}):{max(distance, 0)}"
    return f"({left_str},{right_str})"

def save_newick_files(tree: TreeNode, blosum_version: str, output_dir: str = ".") -> None:
    """Save both Newick variants to files.
    
    Args:
        tree: Root node of the tree
        blosum_version: BLOSUM matrix version (50 or 62)
        output_dir: Directory to save files (default: current)
    """
    # Simple Newick (no distances)
    simple_nwk = to_simple_newick(tree) + ";"
    simple_path = f"{output_dir}/tree_blosum{blosum_version}_newick.nw"
    with open(simple_path, 'w') as f:
        f.write(simple_nwk)
    
    # Newick with distances
    dist_nwk = to_distance_newick(tree) + ";"
    dist_path = f"{output_dir}/tree_blosum{blosum_version}_newick_with_distance.nw"
    with open(dist_path, 'w') as f:
        f.write(dist_nwk)