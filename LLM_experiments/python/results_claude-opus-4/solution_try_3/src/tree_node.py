"""Tree node structure for phylogenetic tree representation."""

from typing import Optional, List, Set, Tuple


class TreeNode:
    """
    Represents a node in the phylogenetic tree.
    
    Can be either a leaf node (species) or internal node (ancestor).
    """
    
    def __init__(
        self,
        name: str,
        height: float = 0.0,
        left: Optional['TreeNode'] = None,
        right: Optional['TreeNode'] = None
    ):
        """
        Initialize a tree node.
        
        Args:
            name: Node identifier (species name for leaves, generated for internal)
            height: Similarity score at which this node was created
            left: Left child node
            right: Right child node
        """
        self.name = name
        self.height = height
        self.left = left
        self.right = right
        self.parent: Optional[TreeNode] = None
        
        # Set parent references for children
        if left:
            left.parent = self
        if right:
            right.parent = self
    
    def is_leaf(self) -> bool:
        """Check if this node is a leaf (has no children)."""
        return self.left is None and self.right is None
    
    def get_leaves(self) -> List['TreeNode']:
        """
        Get all leaf nodes under this node.
        
        Returns:
            List of leaf nodes
        """
        if self.is_leaf():
            return [self]
        
        leaves = []
        if self.left:
            leaves.extend(self.left.get_leaves())
        if self.right:
            leaves.extend(self.right.get_leaves())
        return leaves
    
    def get_leaf_names(self) -> Set[str]:
        """
        Get names of all leaf nodes under this node.
        
        Returns:
            Set of species names
        """
        return {leaf.name for leaf in self.get_leaves()}
    
    def get_max_height(self) -> float:
        """
        Get the maximum height in the subtree rooted at this node.
        
        Returns:
            Maximum height value
        """
        if self.is_leaf():
            return self.height
        
        max_height = self.height
        if self.left:
            max_height = max(max_height, self.left.get_max_height())
        if self.right:
            max_height = max(max_height, self.right.get_max_height())
        return max_height
    
    def to_newick_simple(self) -> str:
        """
        Convert subtree to simple Newick format (no branch lengths).
        
        Returns:
            Simple Newick format representation
        """
        if self.is_leaf():
            return self.name
        
        left_str = self.left.to_newick_simple() if self.left else ""
        right_str = self.right.to_newick_simple() if self.right else ""
        
        return f"({left_str},{right_str})"
    
    def to_newick_with_distances(self, parent_height: Optional[float] = None) -> str:
        """
        Convert subtree to Newick format with branch lengths as integers.
        
        Args:
            parent_height: Height of parent node for branch length calculation
            
        Returns:
            Newick format representation with integer distances
        """
        # Calculate branch length as integer
        if parent_height is not None:
            # Branch length is the difference in heights
            branch_length = int(parent_height - self.height)
        else:
            # Root node, no branch length
            branch_length = 0
        
        if self.is_leaf():
            if parent_height is not None:
                return f"{self.name}:{branch_length}"
            else:
                return self.name
        
        # Recursively process children
        left_str = self.left.to_newick_with_distances(self.height) if self.left else ""
        right_str = self.right.to_newick_with_distances(self.height) if self.right else ""
        
        # Format internal node
        if parent_height is not None:
            return f"({left_str},{right_str}):{branch_length}"
        else:
            # Root node
            return f"({left_str},{right_str})"
    
    def __repr__(self) -> str:
        """String representation of the node."""
        node_type = "Leaf" if self.is_leaf() else "Internal"
        return f"{node_type}Node(name='{self.name}', height={self.height})"