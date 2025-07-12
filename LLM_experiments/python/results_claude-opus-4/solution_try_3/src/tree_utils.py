# Filename: src/tree_utils.py
"""Utility functions for tree analysis and visualization."""

import logging
from typing import List, Dict, Tuple, Set
from pathlib import Path

from .tree_node import TreeNode

logger = logging.getLogger(__name__)


def print_tree_structure(node: TreeNode, prefix: str = "", is_last: bool = True) -> None:
    """
    Print tree structure in a readable format.
    
    Args:
        node: Tree node to print from
        prefix: Prefix for indentation
        is_last: Whether this is the last child
    """
    # Print current node
    connector = "└── " if is_last else "├── "
    print(f"{prefix}{connector}{node.name} (height: {node.height:.2f})")
    
    # Prepare prefix for children
    extension = "    " if is_last else "│   "
    child_prefix = prefix + extension
    
    # Print children
    children = []
    if node.left:
        children.append(node.left)
    if node.right:
        children.append(node.right)
    
    for i, child in enumerate(children):
        is_last_child = (i == len(children) - 1)
        print_tree_structure(child, child_prefix, is_last_child)


def get_tree_statistics(root: TreeNode) -> Dict[str, any]:
    """
    Calculate statistics about the tree.
    
    Args:
        root: Root node of the tree
        
    Returns:
        Dictionary with tree statistics
    """
    all_nodes = []
    leaf_nodes = []
    internal_nodes = []
    
    def traverse(node: TreeNode):
        all_nodes.append(node)
        if node.is_leaf():
            leaf_nodes.append(node)
        else:
            internal_nodes.append(node)
        
        if node.left:
            traverse(node.left)
        if node.right:
            traverse(node.right)
    
    traverse(root)
    
    heights = [node.height for node in internal_nodes]
    
    return {
        "total_nodes": len(all_nodes),
        "leaf_nodes": len(leaf_nodes),
        "internal_nodes": len(internal_nodes),
        "max_height": max(heights) if heights else 0,
        "min_height": min(heights) if heights else 0,
        "species": sorted([node.name for node in leaf_nodes])
    }


def validate_tree(root: TreeNode) -> List[str]:
    """
    Validate tree structure and return any issues found.
    
    Args:
        root: Root node of the tree
        
    Returns:
        List of validation issues (empty if tree is valid)
    """
    issues = []
    
    # def check_node(node: TreeNode, visited: Set[str]) -> None:
    #     # Check for cycles
    #     if node.name in visited:
    #         issues.append(f"Cycle detected at node {node.name}")
    #         return
        
    #     visited.add(node.name)
        
    #     # Check internal node has both children
    #     if not node.is_leaf():
    #         if not node.left or not node.right:
    #             issues.append(f"Internal node {node.name} missing child")
            
    #         # Check height consistency (parent should have higher similarity)
    #         if node.left and node.left.height > node.height:
    #             issues.append(
    #                 f"Height inconsistency: {node.name} ({node.height}) < "
    #                 f"child {node.left.name} ({node.left.height})"
    #             )
    #         if node.right and node.right.height > node.height:
    #             issues.append(
    #                 f"Height inconsistency: {node.name} ({node.height}) < "
    #                 f"child {node.right.name} ({node.right.height})"
    #             )
        
    #     # Recursively check children
    #     if node.left:
    #         check_node(node.left, visited.copy())
    #     if node.