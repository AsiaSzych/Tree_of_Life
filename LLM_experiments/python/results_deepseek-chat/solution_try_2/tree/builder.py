from typing import Dict, Tuple, List, Optional
from .node import TreeNode

class TreeBuilder:
    def __init__(self, similarity_scores: Dict[Tuple[str, str], int]):
        """
        Initialize with precomputed similarity scores.
        
        Args:
            similarity_scores: Dictionary of {(species1, species2): NW score}
        """
        self.similarity_scores = similarity_scores
        self.species = self._get_unique_species()
        self.clusters = {name: TreeNode(name) for name in self.species}
        self.merge_history: List[Tuple[str, str, int]] = []
    
    def _get_unique_species(self) -> List[str]:
        """Extract unique species names from similarity scores."""
        species = set()
        for (s1, s2) in self.similarity_scores.keys():
            species.add(s1)
            species.add(s2)
        return list(species)
    
    def _find_most_similar_pair(self) -> Tuple[str, str, int]:
        """Find the pair of clusters with highest similarity score."""
        max_score = -1
        best_pair = None
        
        # Get current cluster names
        cluster_names = list(self.clusters.keys())
        
        # Check all pairwise combinations
        for i in range(len(cluster_names)):
            for j in range(i+1, len(cluster_names)):
                s1, s2 = cluster_names[i], cluster_names[j]
                score = self.similarity_scores.get((s1, s2), 0)
                if score > max_score:
                    max_score = score
                    best_pair = (s1, s2)
        
        if not best_pair:
            raise ValueError("No similar pairs found")
        
        return (*best_pair, max_score)
    
    def build_tree(self) -> TreeNode:
        """Build phylogenetic tree using single-linkage clustering."""
        while len(self.clusters) > 1:
            # Find most similar pair
            s1, s2, score = self._find_most_similar_pair()
            
            # Create new internal node
            new_name = f"node_{len(self.clusters)}"
            new_node = TreeNode(
                name=new_name,
                height=score,
                left=self.clusters[s1],
                right=self.clusters[s2]
            )
            
            # Update clusters
            del self.clusters[s1]
            del self.clusters[s2]
            self.clusters[new_name] = new_node
            
            # Record merge history
            self.merge_history.append((s1, s2, score))
        
        # Return root node
        return list(self.clusters.values())[0]