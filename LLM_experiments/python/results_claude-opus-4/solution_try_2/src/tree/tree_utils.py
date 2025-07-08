"""
Utility functions for tree operations and analysis.
"""
from typing import List, Dict, Tuple
from .phylogenetic_tree import PhylogeneticTree, TreeNode


def get_tree_statistics(tree: PhylogeneticTree) -> Dict[str, any]:
    """
    Calculate statistics about the phylogenetic tree.
    
    Args:
        tree: PhylogeneticTree object
        
    Returns:
        Dictionary with tree statistics
    """
    if not tree.root:
        return {"error": "Tree has no root"}
    
    def _get_depth(node: TreeNode) -> int:
        """Get maximum depth of subtree."""
        if node.is_leaf:
            return 0
        
        left_depth = _get_depth(node.left) if node.left else 0
        right_depth = _get_depth(node.right) if node.right else 0
        
        return 1 + max(left_depth, right_depth)
    
    def _get_all_heights(node: TreeNode) -> List[float]:
        """Get all merge heights in the tree."""
        heights = []
        if not node.is_leaf:
            heights.append(node.height)
            if node.left:
                heights.extend(_get_all_heights(node.left))
            if node.right:
                heights.extend(_get_all_heights(node.right))
        return heights
    
    leaves = tree.root.get_leaves()
    heights = _get_all_heights(tree.root)
    
    return {
        "num_species": len(leaves),
        "tree_depth": _get_depth(tree.root),
        "root_height": tree.root.height,
        "min_merge_height": min(heights) if heights else 0,
        "max_merge_height": max(heights) if heights else 0,
        "species": sorted(leaves)
    }


def validate_tree_structure(tree: PhylogeneticTree) -> Tuple[bool, List[str]]:
    """
    Validate the tree structure for consistency.
    
    Args:
        tree: PhylogeneticTree object
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    if not tree.root:
        return False, ["Tree has no root"]
    
    def _validate_node(node: TreeNode, parent_height: float = float('inf')) -> None:
        """Recursively validate node properties."""
        # Check height consistency
        if node.height > parent_height:
            errors.append(
                f"Node {node.name} has height {node.height} > parent height {parent_height}"
            )
        
        # Check internal node properties
        if not node.is_leaf:
            if not node.left or not node.right:
                errors.append(f"Internal node {node.name} missing children")
            else:
                _validate_node(node.left, node.height)
                _validate_node(node.right, node.height)
        else:
            # Leaf nodes should have height 0
            if node.height != 0:
                errors.append(f"Leaf node {node.name} has non-zero height {node.height}")
    
    _validate_node(tree.root)
    
    return len(errors) == 0, errors