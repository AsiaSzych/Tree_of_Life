import matplotlib.pyplot as plt
from phylo_tree import TreeNode
from typing import Tuple, Dict, List, Optional

def get_leaves(node: TreeNode) -> List[str]:
    if node.is_leaf():
        return [node.name]
    return get_leaves(node.left) + get_leaves(node.right)

def plot_dendrogram(
    root: TreeNode,
    blosum_version: str,
    output_dir: str = ".",
    figsize: Tuple[int, int] = (12, 6),
) -> None:
    leaves = get_leaves(root)
    n_leaves = len(leaves)
    leaf_positions: Dict[str, float] = {
        name: i for i, name in enumerate(leaves)
    }
    fig, ax = plt.subplots(figsize=figsize)
    def draw_node(
        node: TreeNode, parent_height: Optional[int] = None
    ) -> float:
        if node.is_leaf():
            x = node.height if node.height is not None else 0
            y = leaf_positions[node.name]
            ax.text(
                x - 0.01 * max(1, x), y, node.name,
                va="center", ha="right", fontsize=10
            )
            return y
        left_y = draw_node(node.left, node.height)
        right_y = draw_node(node.right, node.height)
        y = (left_y + right_y) / 2
        x = node.height if node.height is not None else 0
        ax.plot([x, x], [left_y, right_y], color="k")
        for child, child_y in [(node.left, left_y), (node.right, right_y)]:
            child_x = (
                child.height if child.height is not None else 0
            ) if not child.is_leaf() else 0
            ax.plot([child_x, x], [child_y, child_y], color="k")
        return y
    draw_node(root)
    ax.set_ylim(-1, n_leaves)
    ax.set_xlim(left=0)
    ax.invert_xaxis()
    ax.set_xlabel("Needleman-Wunsch similarity score")
    ax.set_ylabel("Species")
    ax.set_yticks([])
    ax.set_title(f"Phylogenetic Tree (BLOSUM{blosum_version})")
    plt.tight_layout()
    output_path = f"{output_dir}/phylogenetic_tree_blosum{blosum_version}.png"
    plt.savefig(output_path, dpi=150)
    plt.close(fig)