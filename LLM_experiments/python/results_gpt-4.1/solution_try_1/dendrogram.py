import matplotlib.pyplot as plt
from tree import TreeNode
from typing import Optional, Tuple, Dict


def _plot_dendrogram(
    node: TreeNode,
    ax: plt.Axes,
    y_positions: Dict[str, float],
    x_offset: int = 0,
    y_step: float = 1.0,
    current_y: Optional[float] = None,
    parent_x: Optional[int] = None,
    parent_y: Optional[float] = None,
) -> Tuple[float, float]:
    if node.is_leaf():
        y = y_positions[node.label]
        x = 0 if node.height is None else node.height
        if parent_x is not None:
            ax.plot([parent_x, x], [parent_y, y], color="k")
        ax.text(x - 5, y, node.label, va="center", ha="right", fontsize=10)
        return x, y

    left_x, left_y = _plot_dendrogram(
        node.left, ax, y_positions, x_offset, y_step, None, node.height, None
    )
    right_x, right_y = _plot_dendrogram(
        node.right, ax, y_positions, x_offset, y_step, None, node.height, None
    )

    x = node.height if node.height is not None else 0
    y = (left_y + right_y) / 2

    ax.plot([x, x], [left_y, right_y], color="k")
    if parent_x is not None:
        ax.plot([parent_x, x], [parent_y, y], color="k")
    ax.plot([x, left_x], [left_y, left_y], color="k")
    ax.plot([x, right_x], [right_y, right_y], color="k")

    return x, y


def draw_dendrogram(
    root: TreeNode,
    filename: str,
    figsize: Tuple[int, int] = (10, 6)
):
    leaves = []

    def collect_leaves(node: TreeNode):
        if node.is_leaf():
            leaves.append(node.label)
        else:
            collect_leaves(node.left)
            collect_leaves(node.right)

    collect_leaves(root)
    y_positions = {label: i for i, label in enumerate(leaves)}

    fig, ax = plt.subplots(figsize=figsize)
    _plot_dendrogram(root, ax, y_positions)

    ax.set_ylim(-1, len(leaves))
    max_score = root.height if root.height is not None else 0
    ax.set_xlim(-0.05 * max_score, 1.05 * max_score)
    ax.set_xlabel("Needleman-Wunsch Similarity Score")
    ax.set_ylabel("Species")
    ax.set_yticks([])
    ax.set_title("Phylogenetic Tree Dendrogram")
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close(fig)
    print(f"Dendrogram saved to {filename}")