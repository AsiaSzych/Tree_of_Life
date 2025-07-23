"""
Data structures for phylogenetic tree representation.
"""
from typing import Optional, List, Union, Tuple
from dataclasses import dataclass, field


@dataclass
class TreeNode:
    """Represents a node in the phylogenetic tree."""
    
    name: Optional[str] = None  # Species name for leaf nodes, None for internal nodes
    height: float = 0.0  # Similarity score at which this node was created
    children: List['TreeNode'] = field(default_factory=list)
    parent: Optional['TreeNode'] = None
    
    def is_leaf(self) -> bool:
        """Check if this is a leaf node (species)."""
        return len(self.children) == 0
    
    def is_root(self) -> bool:
        """Check if this is the root node."""
        return self.parent is None
    
    def get_leaves(self) -> List['TreeNode']:
        """Get all leaf nodes (species) under this node."""
        if self.is_leaf():
            return [self]
        
        leaves = []
        for child in self.children:
            leaves.extend(child.get_leaves())
        return leaves
    
    def get_species_names(self) -> List[str]:
        """Get names of all species under this node."""
        return [leaf.name for leaf in self.get_leaves() if leaf.name]
    
    def add_child(self, child: 'TreeNode'):
        """Add a child node and set parent relationship."""
        self.children.append(child)
        child.parent = self
    
    def get_newick_simple(self) -> str:
        """Convert subtree to simple Newick format (names only)."""
        if self.is_leaf():
            return self.name or ""
        
        # Recursively get Newick strings for children
        child_strings = [child.get_newick_simple() for child in self.children]
        return f"({','.join(child_strings)})"
    
    def get_newick_with_distances(self) -> str:
        """Convert subtree to Newick format with branch distances."""
        if self.is_leaf():
            return self.name or ""
        
        # Recursively get Newick strings for children
        child_strings = []
        for child in self.children:
            child_newick = child.get_newick_with_distances()
            # Calculate branch length as difference in heights
            # Use integer values as required
            branch_length = int(self.height - child.height)
            child_strings.append(f"{child_newick}:{branch_length}")
        
        return f"({','.join(child_strings)})"
    
    def find_clusters_at_threshold(self, threshold: float) -> List[List[str]]:
        """Find clusters by cutting the tree at a given similarity threshold."""
        if self.height < threshold:
            # This entire subtree is below threshold, return all species as one cluster
            return [self.get_species_names()]
        
        if self.is_leaf():
            # Leaf node above threshold
            return [[self.name]] if self.name else []
        
        # Internal node above threshold, check children
        clusters = []
        for child in self.children:
            clusters.extend(child.find_clusters_at_threshold(threshold))
        
        return clusters


@dataclass
class PhylogeneticTree:
    """Represents the complete phylogenetic tree."""
    
    root: Optional[TreeNode] = None
    
    def get_newick_simple(self) -> str:
        """Get the tree in simple Newick format (names only)."""
        if not self.root:
            return ""
        return self.root.get_newick_simple() + ";"
    
    def get_newick_with_distances(self) -> str:
        """Get the tree in Newick format with branch distances."""
        if not self.root:
            return ""
        return self.root.get_newick_with_distances() + ";"
    
    def get_clusters_at_threshold(self, threshold: float) -> List[List[str]]:
        """Get clusters by cutting tree at similarity threshold."""
        if not self.root:
            return []
        return self.root.find_clusters_at_threshold(threshold)
    
    def get_all_nodes(self) -> List[TreeNode]:
        """Get all nodes in the tree (for visualization)."""
        if not self.root:
            return []
        
        nodes = []
        to_visit = [self.root]
        
        while to_visit:
            node = to_visit.pop(0)
            nodes.append(node)
            to_visit.extend(node.children)
        
        return nodess