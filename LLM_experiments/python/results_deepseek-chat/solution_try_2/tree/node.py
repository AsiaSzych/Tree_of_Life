from typing import Optional, List

class TreeNode:
    def __init__(self, 
                 name: str, 
                 height: int = 0,
                 left: Optional['TreeNode'] = None,
                 right: Optional['TreeNode'] = None):
        self.name = name
        self.height = height  # NW similarity score
        self.left = left
        self.right = right
    
    def is_leaf(self) -> bool:
        return self.left is None and self.right is None
    
    def get_simple_newick(self) -> str:
        """Generate Newick format without branch lengths."""
        if self.is_leaf():
            return self.name
        left_str = self.left.get_simple_newick()
        right_str = self.right.get_simple_newick()
        return f"({left_str},{right_str})"
    
    def get_newick_with_distances(self) -> str:
        """Generate Newick format with branch lengths (integer NW scores)."""
        if self.is_leaf():
            return f"{self.name}:0"  # Leaves have 0 branch length
        
        left_str = self.left.get_newick_with_distances()
        right_str = self.right.get_newick_with_distances()
        
        # Calculate branch lengths (difference between node heights)
        left_length = self.height - self.left.height
        right_length = self.height - self.right.height
        
        return f"({left_str}:{left_length},{right_str}:{right_length})"
    
    def get_leaves(self) -> List['TreeNode']:
        """Get all leaf nodes under this node."""
        if self.is_leaf():
            return [self]
        return self.left.get_leaves() + self.right.get_leaves()