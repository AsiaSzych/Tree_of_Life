import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram, to_tree
from typing import Dict, List, Any, Tuple

class PhylogeneticTree:
    def __init__(self, similarity_scores: Dict[Tuple[str, str], int]):
        self.species = list({s for pair in similarity_scores.keys() for s in pair})
        self.similarity_scores = similarity_scores
        self.linkage_matrix = None
        self.root = None

    def build_tree(self):
        """Build phylogenetic tree using single linkage clustering."""
        dist_matrix = self._create_distance_matrix()
        self.linkage_matrix = linkage(dist_matrix, method='single')
        self.root = to_tree(self.linkage_matrix)

    def _create_distance_matrix(self) -> np.ndarray:
        """Convert similarity scores to distance matrix."""
        n = len(self.species)
        dist_matrix = np.zeros((n, n))
        species_idx = {s: i for i, s in enumerate(self.species)}
        max_score = max(self.similarity_scores.values())
        
        for (s1, s2), score in self.similarity_scores.items():
            i, j = species_idx[s1], species_idx[s2]
            dist_matrix[i, j] = dist_matrix[j, i] = max_score - score
        return dist_matrix

    def plot_dendrogram(self, blosum_type: str):
        """Save horizontal dendrogram to file."""
        plt.figure(figsize=(10, 8))
        dendrogram(
            self.linkage_matrix,
            labels=self.species,
            orientation='left',
            distance_sort='descending'
        )
        plt.title(f'Phylogenetic Tree (BLOSUM{blosum_type})')
        plt.xlabel('Needleman-Wunsch Similarity Score')
        plt.tight_layout()
        plt.savefig(f'./outputs/phylogenetic_tree_blosum{blosum_type}.png', dpi=300)
        plt.close()

    def get_clusters_at_threshold(self, threshold: int) -> List[List[str]]:
        """Get species clusters at given NW score threshold."""
        clusters = []
        
        def traverse(node):
            if node.is_leaf():
                return [self.species[node.id]]
            
            left = traverse(node.left)
            right = traverse(node.right)
            node_score = max(self.similarity_scores.values()) - node.dist
            
            if node_score >= threshold:
                return left + right
            else:
                if left: clusters.append(left)
                if right: clusters.append(right)
                return []
        
        root_cluster = traverse(self.root)
        if root_cluster: clusters.append(root_cluster)
        return clusters

    def get_simple_newick(self, node: Any = None) -> str:
        """Generate Newick format without distances.
        
        Args:
            node: Current node (defaults to root)
            
        Returns:
            Newick format string without branch lengths
        """
        if node is None:
            node = self.root
            
        if node.is_leaf():
            return self.species[node.id]
        else:
            left = self.get_simple_newick(node.left)
            right = self.get_simple_newick(node.right)
            return f"({left},{right})"

    def get_distance_newick(self, node: Any = None, parent_dist: int = 0) -> str:
        """Generate Newick format with integer distances.
        
        Args:
            node: Current node (defaults to root)
            parent_dist: Distance to parent node
            
        Returns:
            Newick format string with integer branch lengths
        """
        if node is None:
            node = self.root
            
        if node.is_leaf():
            return f"{self.species[node.id]}:{int(parent_dist - node.dist)}"
        else:
            left = self.get_distance_newick(node.left, node.dist)
            right = self.get_distance_newick(node.right, node.dist)
            return f"({left},{right}):{int(parent_dist - node.dist)}"   