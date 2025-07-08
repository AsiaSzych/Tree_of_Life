"""
Module for exporting phylogenetic trees to Newick format.
"""
from pathlib import Path
from typing import Optional
from .phylogenetic_tree import TreeNode, PhylogeneticTree


def node_to_newick_simple(node: TreeNode) -> str:
    """
    Convert tree node to simple Newick format (names only).
    
    Args:
        node: TreeNode to convert
        
    Returns:
        Newick string without distances
    """
    if node.is_leaf:
        return node.name
    
    left_str = node_to_newick_simple(node.left) if node.left else ""
    right_str = node_to_newick_simple(node.right) if node.right else ""
    
    return f"({left_str},{right_str})"


def node_to_newick_with_distances(node: TreeNode, parent_height: Optional[float] = None) -> str:
    """
    Convert tree node to Newick format with branch distances.
    
    Args:
        node: TreeNode to convert
        parent_height: Height of parent node for distance calculation
        
    Returns:
        Newick string with distances
    """
    # Calculate branch length (distance from parent)
    if parent_height is not None:
        # Branch length is the difference in heights
        # Since we're using similarity (higher = more similar), 
        # distance is parent_height - node_height
        branch_length = int(parent_height - node.height)
    else:
        branch_length = 0
    
    if node.is_leaf:
        # For leaves, include the branch length to parent
        return f"{node.name}:{branch_length}"
    
    # Recursively process children
    left_str = node_to_newick_with_distances(node.left, node.height) if node.left else ""
    right_str = node_to_newick_with_distances(node.right, node.height) if node.right else ""
    
    # Format internal node
    if parent_height is not None:
        return f"({left_str},{right_str}):{branch_length}"
    else:
        # Root node - no branch length
        return f"({left_str},{right_str})"


def save_tree_to_newick(tree: PhylogeneticTree, blosum_version: str, output_dir: str = "."):
    """
    Save phylogenetic tree to both Newick format files.
    
    Args:
        tree: PhylogeneticTree object to save
        blosum_version: BLOSUM version used (e.g., "blosum50", "blosum62")
        output_dir: Directory to save output files
    """
    if not tree.root:
        raise ValueError("Tree has no root node")
    
    # Ensure output directory exists
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Generate simple Newick (names only)
    simple_newick = node_to_newick_simple(tree.root) + ";"
    simple_filename = output_path / f"tree_{blosum_version}_newick.nw"
    
    with open(simple_filename, 'w') as f:
        f.write(simple_newick)
    
    print(f"Saved simple Newick format to: {simple_filename}")
    
    # Generate Newick with distances
    distance_newick = node_to_newick_with_distances(tree.root) + ";"
    distance_filename = output_path / f"tree_{blosum_version}_newick_with_distance.nw"
    
    with open(distance_filename, 'w') as f:
        f.write(distance_newick)
    
    print(f"Saved Newick with distances to: {distance_filename}")
    
    return simple_filename, distance_filename


def extract_blosum_version_from_scores_file(scores_file: str) -> str:
    """
    Extract BLOSUM version from scores filename.
    
    Args:
        scores_file: Path to scores file (e.g., "organisms_scores_blosum62.json")
        
    Returns:
        BLOSUM version string (e.g., "blosum62")
    """
    filename = Path(scores_file).stem  # Remove .json extension
    # Extract blosum version from filename pattern "organisms_scores_blosumXX"
    parts = filename.split('_')
    if len(parts) >= 3 and parts[-1].startswith('blosum'):
        return parts[-1]
    else:
        # Default fallback
        return "blosum62"