# filename: visualization.py
from typing import List, Dict
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram
from pathlib import Path
from clustering import Node

def _build_linkage_matrix_recursive(node: Node, linkage_list: list, leaf_map: Dict[str, int], node_map: Dict[int, int]) -> int:
    if node.is_leaf:
        leaf_index = leaf_map[node.species_name]
        node_map[node.id] = leaf_index
        return leaf_index
    child1, child2 = node.children
    child1_idx = _build_linkage_matrix_recursive(child1, linkage_list, leaf_map, node_map)
    child2_idx = _build_linkage_matrix_recursive(child2, linkage_list, leaf_map, node_map)
    distance = np.float64(node.value)
    cluster_size = len(node.get_all_species())
    linkage_list.append([child1_idx, child2_idx, distance, cluster_size])
    new_cluster_idx = len(leaf_map) + len(linkage_list) - 1
    node_map[node.id] = new_cluster_idx
    return new_cluster_idx

def tree_to_linkage_matrix(root_node: Node, species_labels: List[str]) -> np.ndarray:
    leaf_map = {name: i for i, name in enumerate(species_labels)}
    linkage_list, node_map = [], {}
    _build_linkage_matrix_recursive(root_node, linkage_list, leaf_map, node_map)
    return np.array(linkage_list)

def draw_dendrogram(root_node: Node, species_labels: List[str], output_path: Path):
    print(f"Generating dendrogram and saving to {output_path}...")
    linkage_matrix = tree_to_linkage_matrix(root_node, species_labels)
    fig, ax = plt.subplots(figsize=(12, 8))
    dendrogram(Z=linkage_matrix, labels=species_labels, orientation='right', ax=ax, color_threshold=0, above_threshold_color='black')
    ax.set_title('Phylogenetic Tree Dendrogram', fontsize=16)
    ax.set_xlabel('Needleman-Wunsch Similarity Score', fontsize=12)
    ax.set_ylabel('Species', fontsize=12)
    ax.grid(axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300)
        print("Dendrogram saved successfully.")
    except IOError as e:
        print(f"Error saving dendrogram: {e}")
    finally:
        plt.close(fig)