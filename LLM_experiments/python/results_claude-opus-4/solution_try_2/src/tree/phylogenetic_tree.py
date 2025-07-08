"""
Phylogenetic tree construction using single-linkage clustering with similarity scores.
"""
import json
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from pathlib import Path
import heapq


@dataclass
class TreeNode:
    """
    Represents a node in the phylogenetic tree.
    
    Attributes:
        name: Node identifier (species name for leaves, generated for internal nodes)
        height: Similarity score at which this node was created
        left: Left child node
        right: Right child node
        is_leaf: Whether this is a leaf node (original species)
    """
    name: str
    height: float
    left: Optional['TreeNode'] = None
    right: Optional['TreeNode'] = None
    is_leaf: bool = True
    
    def get_leaves(self) -> List[str]:
        """Get all leaf nodes (species) under this node."""
        if self.is_leaf:
            return [self.name]
        
        leaves = []
        if self.left:
            leaves.extend(self.left.get_leaves())
        if self.right:
            leaves.extend(self.right.get_leaves())
        return leaves
    
    def get_max_leaf_height(self) -> float:
        """Get the maximum height among all leaves in this subtree."""
        if self.is_leaf:
            return self.height
        
        max_height = 0
        if self.left:
            max_height = max(max_height, self.left.get_max_leaf_height())
        if self.right:
            max_height = max(max_height, self.right.get_max_leaf_height())
        
        return max_height


class PhylogeneticTree:
    """
    Phylogenetic tree built using single-linkage clustering with similarity scores.
    """
    
    def __init__(self, scores_file: str):
        """
        Initialize the tree builder with similarity scores.
        
        Args:
            scores_file: Path to JSON file with pairwise similarity scores
        """
        self.scores_file = scores_file
        self.pairwise_scores = self._load_scores()
        self.root: Optional[TreeNode] = None
        self._max_self_similarity = 0
        self._build_tree()
    
    def _load_scores(self) -> Dict[str, int]:
        """Load similarity scores from JSON file."""
        with open(self.scores_file, 'r') as f:
            return json.load(f)
    
    def _parse_species_from_scores(self) -> Set[str]:
        """Extract unique species names from score keys."""
        species = set()
        for key in self.pairwise_scores.keys():
            sp1, sp2 = key.split('_', 1)
            species.add(sp1)
            species.add(sp2)
        return species
    
    def _get_similarity(self, species1: str, species2: str) -> int:
        """Get similarity score between two species."""
        key1 = f"{species1}_{species2}"
        key2 = f"{species2}_{species1}"
        
        if key1 in self.pairwise_scores:
            return self.pairwise_scores[key1]
        elif key2 in self.pairwise_scores:
            return self.pairwise_scores[key2]
        else:
            raise KeyError(f"No score found for pair: {species1}, {species2}")
    
    def _get_cluster_similarity(self, cluster1: TreeNode, cluster2: TreeNode) -> int:
        """
        Calculate similarity between two clusters using single linkage.
        Single linkage = maximum similarity between any pair of species.
        """
        leaves1 = cluster1.get_leaves()
        leaves2 = cluster2.get_leaves()
        
        max_similarity = float('-inf')
        
        for sp1 in leaves1:
            for sp2 in leaves2:
                similarity = self._get_similarity(sp1, sp2)
                max_similarity = max(max_similarity, similarity)
        
        return max_similarity
    
    def _build_tree(self):
        """Build the phylogenetic tree using agglomerative clustering."""
        # Initialize clusters - each species is its own cluster
        species_list = list(self._parse_species_from_scores())
        
        # Find maximum self-similarity for proper height initialization
        self._max_self_similarity = max(
            self._get_similarity(sp, sp) for sp in species_list
        )
        
        # Initialize leaf nodes with their self-similarity as height
        clusters = {
            species: TreeNode(
                name=species, 
                height=self._get_similarity(species, species), 
                is_leaf=True
            )
            for species in species_list
        }
        
        # Priority queue for efficient finding of most similar pairs
        # Use negative similarity for max-heap behavior
        similarity_heap = []
        cluster_id_counter = 0
        
        # Calculate initial similarities between all pairs
        cluster_names = list(clusters.keys())
        for i in range(len(cluster_names)):
            for j in range(i + 1, len(cluster_names)):
                name1, name2 = cluster_names[i], cluster_names[j]
                similarity = self._get_similarity(name1, name2)
                # Push negative similarity for max-heap behavior
                heapq.heappush(similarity_heap, (-similarity, name1, name2))
        
        # Merge clusters until only one remains
        while len(clusters) > 1:
            # Find pair with highest similarity
            while similarity_heap:
                neg_similarity, name1, name2 = heapq.heappop(similarity_heap)
                similarity = -neg_similarity
                
                # Check if both clusters still exist (not already merged)
                if name1 in clusters and name2 in clusters:
                    break
            else:
                raise RuntimeError("No valid pairs found for merging")
            
            # Create new internal node
            cluster_id_counter += 1
            new_name = f"internal_{cluster_id_counter}"
            
            new_node = TreeNode(
                name=new_name,
                height=similarity,  # Height is the similarity score
                left=clusters[name1],
                right=clusters[name2],
                is_leaf=False
            )
            
            # Remove merged clusters
            del clusters[name1]
            del clusters[name2]
            
            # Add new cluster
            clusters[new_name] = new_node
            
            # Calculate similarities between new cluster and remaining clusters
            for other_name in clusters:
                if other_name != new_name:
                    similarity = self._get_cluster_similarity(
                        clusters[new_name], 
                        clusters[other_name]
                    )
                    heapq.heappush(similarity_heap, (-similarity, new_name, other_name))
        
        # Set root to the final remaining cluster
        self.root = list(clusters.values())[0]
    
    def get_clusters_at_threshold(self, threshold: int) -> List[List[str]]:
        """
        Get clusters by cutting the tree at a given similarity threshold.
        
        Args:
            threshold: Similarity threshold for clustering
            
        Returns:
            List of clusters, where each cluster is a list of species names
        """
        if not self.root:
            return []
        
        def _traverse_and_cut(node: TreeNode, threshold: int) -> List[List[str]]:
            """Recursively traverse tree and cut at threshold."""
            # If this node's height is below threshold, return all leaves as one cluster
            if node.height <= threshold:
                return [node.get_leaves()]
            
            # Otherwise, recursively process children
            clusters = []
            
            if node.left:
                if node.left.is_leaf or node.left.height <= threshold:
                    clusters.append(node.left.get_leaves())
                else:
                    clusters.extend(_traverse_and_cut(node.left, threshold))
            
            if node.right:
                if node.right.is_leaf or node.right.height <= threshold:
                    clusters.append(node.right.get_leaves())
                else:
                    clusters.extend(_traverse_and_cut(node.right, threshold))
            
            return clusters
        
        return _traverse_and_cut(self.root, threshold)
    
    def get_merge_history(self) -> List[Tuple[str, str, float]]:
        """
        Get the history of merges in the tree.
        
        Returns:
            List of tuples (left_cluster, right_cluster, merge_height)
        """
        history = []
        
        def _traverse(node: TreeNode):
            if not node.is_leaf:
                left_name = node.left.name if node.left else "None"
                right_name = node.right.name if node.right else "None"
                history.append((left_name, right_name, node.height))
                
                if node.left:
                    _traverse(node.left)
                if node.right:
                    _traverse(node.right)
        
        if self.root:
            _traverse(self.root)
        
        # Sort by merge height (descending - highest similarity first)
        history.sort(key=lambda x: x[2], reverse=True)
        return history


def build_phylogenetic_tree(scores_file: str) -> PhylogeneticTree:
    """
    Convenience function to build a phylogenetic tree from a scores file.
    
    Args:
        scores_file: Path to JSON file with pairwise similarity scores
        
    Returns:
        PhylogeneticTree object
    """
    return PhylogeneticTree(scores_file)