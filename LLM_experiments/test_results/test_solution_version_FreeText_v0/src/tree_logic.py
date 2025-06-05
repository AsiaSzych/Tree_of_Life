# src/tree_logic.py

import numpy as np
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import linkage
from typing import Dict, Tuple, List

class TreeNode:
    """
    Represents a node in the phylogenetic tree.
    """
    def __init__(self, name: str = None, children: List['TreeNode'] = None,
                 branch_length: float = 0.0, nw_score_at_merge: int = None,
                 height: float = 0.0):
        """
        Initializes a TreeNode.

        Args:
            name (str, optional): The name of the species if it's a leaf node, or an internal
                                  node identifier. Defaults to None.
            children (List[TreeNode], optional): A list of child TreeNode objects. Defaults to None.
            branch_length (float, optional): The length of the branch connecting this node to its parent.
                                            For the root, this is 0. Defaults to 0.0.
            nw_score_at_merge (int, optional): For internal nodes, the Needleman-Wunsch similarity score
                                               of the two clusters that were merged to form this node.
                                               Defaults to None.
            height (float, optional): The distance from the "bottom" (leaves at height 0) to this
                                      node's merge point. Defaults to 0.0.
        """
        self.name = name
        self.children = children if children is not None else []
        self.branch_length = branch_length
        self.nw_score_at_merge = nw_score_at_merge
        self.is_leaf = (name is not None and not self.children)
        self.height = height

    def __repr__(self):
        if self.is_leaf:
            return f"Leaf(name='{self.name}', bl={self.branch_length:.2f})"
        return (f"Internal(name='{self.name}', children={len(self.children)}, "
                f"bl={self.branch_length:.2f}, height={self.height:.2f}, nw_score={self.nw_score_at_merge})")

def build_phylogenetic_tree(
    pairwise_scores: Dict[Tuple[str, str], int],
    species_names: List[str]
) -> Tuple[TreeNode, np.ndarray, List[str]]:
    """
    Builds a phylogenetic tree (TreeNode structure) from pairwise Needleman-Wunsch scores
    using agglomerative hierarchical clustering (UPGMA).

    Args:
        pairwise_scores (Dict[Tuple[str, str], int]): Dictionary of (species1, species2) -> score.
        species_names (List[str]): A sorted list of all unique species names.

    Returns:
        Tuple[TreeNode, np.ndarray, List[str]]: A tuple containing:
            - TreeNode: The root node of the constructed phylogenetic tree.
            - np.ndarray: The linkage matrix (Z) from scipy.cluster.hierarchy.linkage.
            - List[str]: The sorted list of species names used for indexing.

    Raises:
        ValueError: If there are fewer than two species to build a tree.
    """
    if len(species_names) < 2:
        raise ValueError("Cannot build a tree with fewer than two species.")

    max_score = max(pairwise_scores.values()) if pairwise_scores else 0

    name_to_idx = {name: i for i, name in enumerate(species_names)}

    num_species = len(species_names)
    distance_matrix = np.zeros((num_species, num_species))

    for (s1, s2), score in pairwise_scores.items():
        idx1 = name_to_idx[s1]
        idx2 = name_to_idx[s2]
        distance = max_score - score
        distance_matrix[idx1, idx2] = distance
        distance_matrix[idx2, idx1] = distance

    condensed_distance_matrix = squareform(distance_matrix)

    linkage_matrix = linkage(condensed_distance_matrix, method='average')

    nodes: List[TreeNode] = [
        TreeNode(name=name, height=0.0) for name in species_names
    ]

    internal_node_counter = 0

    for i, row in enumerate(linkage_matrix):
        idx1, idx2, dist, _ = row
        idx1, idx2 = int(idx1), int(idx2)

        child1 = nodes[idx1]
        child2 = nodes[idx2]

        new_node_height = dist

        child1.branch_length = new_node_height - child1.height
        child2.branch_length = new_node_height - child2.height

        nw_score_at_merge = max_score - new_node_height

        internal_node_name = f"Internal_{internal_node_counter}"
        internal_node_counter += 1

        new_internal_node = TreeNode(
            name=internal_node_name,
            children=[child1, child2],
            branch_length=0.0,
            nw_score_at_merge=nw_score_at_merge,
            height=new_node_height
        )
        nodes.append(new_internal_node)

    root_node = nodes[-1]
    return root_node, linkage_matrix, species_names

def generate_newick(node: TreeNode, include_distances: bool) -> str:
    """
    Recursively generates the Newick string representation of the phylogenetic tree.

    Args:
        node (TreeNode): The current node to process.
        include_distances (bool): Whether to include branch lengths in the Newick string.

    Returns:
        str: The Newick string for the subtree rooted at 'node'.
    """
    if node.is_leaf:
        newick_str = node.name
    else:
        children_newick = [generate_newick(child, include_distances) for child in node.children]
        newick_str = f"({','.join(children_newick)}){node.name}"

    if include_distances and node.branch_length is not None:
        newick_str += f":{node.branch_length:.6f}"

    return newick_str