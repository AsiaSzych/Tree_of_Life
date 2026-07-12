from typing import List, Dict
from phylo_tree import TreeNode

def get_clusters_for_threshold(root: TreeNode, threshold: int) -> List[List[str]]:
    clusters = []
    def traverse(node: TreeNode):
        if node.height is not None and node.height > threshold:
            clusters.append(sorted(list(node.members)))
            return
        if node.is_leaf():
            clusters.append([node.name])
            return
        if node.left:
            traverse(node.left)
        if node.right:
            traverse(node.right)
    traverse(root)
    return clusters

def read_thresholds(filepath: str) -> List[int]:
    thresholds = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                thresholds.append(int(line))
    return thresholds

def get_all_clusters(root: TreeNode, thresholds: List[int]) -> Dict[int, List[List[str]]]:
    result = {}
    for t in thresholds:
        clusters = get_clusters_for_threshold(root, t)
        result[t] = clusters
    return result

def save_clusters_to_json(clusters: Dict[int, List[List[str]]], blosum_version: str, output_dir: str = ".") -> None:
    import json
    output_path = f"{output_dir}/clusters_for_blosum{blosum_version}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(clusters, f, indent=2)