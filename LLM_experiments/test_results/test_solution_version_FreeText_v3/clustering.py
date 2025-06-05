# filename: clustering.py
from typing import Dict, FrozenSet, List, Set, Optional, Tuple

class Node:
    _id_counter = 0
    def __init__(self, children: Tuple['Node', ...], value: Optional[float]):
        self.id = Node._id_counter
        Node._id_counter += 1
        self.children = children
        self.value = value
    @property
    def is_leaf(self) -> bool: return not self.children
    def get_all_species(self) -> Set[str]:
        if self.is_leaf: return set()
        species_set = set()
        for child in self.children: species_set.update(child.get_all_species())
        return species_set
    def __repr__(self) -> str: return f"Node(id={self.id}, value={self.value})"

class LeafNode(Node):
    def __init__(self, species_name: str, value: float):
        super().__init__(children=(), value=value)
        self.species_name = species_name
    def get_all_species(self) -> Set[str]: return {self.species_name}
    def __repr__(self) -> str: return f"Leaf(id={self.id}, species='{self.species_name}')"

class InternalNode(Node):
    def __init__(self, child1: Node, child2: Node, value: float):
        super().__init__(children=(child1, child2), value=value)
    def __repr__(self) -> str:
        return f"Internal(id={self.id}, value={self.value:.2f}, species_count={len(self.get_all_species())})"

def _to_newick_recursive(node: Node, parent_value: Optional[float], with_distance: bool) -> str:
    if node.is_leaf:
        name = node.species_name.replace(" ", "_")
        if with_distance:
            branch_length = abs(node.value - parent_value)
            return f"{name}:{branch_length:.4f}"
        return name
    child_strings = [_to_newick_recursive(child, node.value, with_distance) for child in node.children]
    node_name = f"Node{node.id}"
    subtree = f"({','.join(child_strings)}){node_name}"
    if with_distance:
        branch_length = abs(node.value - parent_value) if parent_value is not None else 0.0
        return f"{subtree}:{branch_length:.4f}"
    return subtree

def tree_to_newick(root_node: Node, with_distance: bool = False) -> str:
    if not root_node: return ""
    newick_str = _to_newick_recursive(root_node, root_node.value, with_distance)
    return f"{newick_str};"

def build_tree(similarity_scores: Dict[FrozenSet[str], float]) -> Optional[Node]:
    if not similarity_scores: return None
    max_score = max(similarity_scores.values()) if similarity_scores else 0
    all_species = sorted(list(set(s for pair in similarity_scores for s in pair)))
    if not all_species: return None
    active_clusters = {node.id: node for node in [LeafNode(name, value=max_score) for name in all_species]}
    species_to_node_id = {node.species_name: node.id for node in active_clusters.values()}
    node_similarities = {frozenset({species_to_node_id[s1], species_to_node_id[s2]}): score for (s1, s2), score in similarity_scores.items()}
    while len(active_clusters) > 1:
        if not node_similarities: break
        pair_to_merge_ids = max(node_similarities, key=node_similarities.get)
        merge_score = node_similarities.pop(pair_to_merge_ids)
        id1, id2 = tuple(pair_to_merge_ids)
        node1, node2 = active_clusters.pop(id1), active_clusters.pop(id2)
        new_node = InternalNode(node1, node2, merge_score)
        active_clusters[new_node.id] = new_node
        new_sims = {}
        for other_id in active_clusters:
            if other_id == new_node.id: continue
            sim1 = node_similarities.get(frozenset({id1, other_id}), -float('inf'))
            sim2 = node_similarities.get(frozenset({id2, other_id}), -float('inf'))
            new_sims[frozenset({new_node.id, other_id})] = max(sim1, sim2)
        keys_to_remove = {k for k in node_similarities if id1 in k or id2 in k}
        for k in keys_to_remove: node_similarities.pop(k, None)
        node_similarities.update(new_sims)
    return list(active_clusters.values())[0]

def get_clusters_at_threshold(root_node: Node, threshold: float) -> List[List[str]]:
    clusters, nodes_to_visit = [], [root_node]
    while nodes_to_visit:
        current_node = nodes_to_visit.pop(0)
        if current_node.value > threshold or current_node.is_leaf:
            clusters.append(sorted(list(current_node.get_all_species())))
        else:
            nodes_to_visit.extend(current_node.children)
    return sorted(clusters)