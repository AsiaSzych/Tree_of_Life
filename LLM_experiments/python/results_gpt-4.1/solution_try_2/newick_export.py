from typing import Optional
from phylo_tree import TreeNode

def to_newick(node: TreeNode) -> str:
    if node.is_leaf():
        return node.name
    left = to_newick(node.left)
    right = to_newick(node.right)
    return f"({left},{right})"

def to_newick_with_distances(node: TreeNode, parent_height: Optional[int] = None) -> str:
    if node.is_leaf():
        if parent_height is not None:
            return f"{node.name}:{int(parent_height)}"
        else:
            return node.name
    left = to_newick_with_distances(node.left, node.height)
    right = to_newick_with_distances(node.right, node.height)
    if parent_height is not None:
        branch_length = int(parent_height - node.height)
        return f"({left},{right}):{branch_length}"
    else:
        return f"({left},{right})"

def save_newick_files(
    root: TreeNode, blosum_version: str, output_dir: str = "."
) -> None:
    newick_str = to_newick(root) + ";"
    newick_path = f"{output_dir}/tree_blosum{blosum_version}_newick.nw"
    with open(newick_path, "w", encoding="utf-8") as f:
        f.write(newick_str)
    newick_dist_str = to_newick_with_distances(root) + ";"
    newick_dist_path = f"{output_dir}/tree_blosum{blosum_version}_newick_with_distance.nw"
    with open(newick_dist_path, "w", encoding="utf-8") as f:
        f.write(newick_dist_str)