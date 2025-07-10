from typing import List, Dict, Optional, Set, Tuple
import matplotlib.pyplot as plt

class TreeNode:
    def __init__(
        self,
        name: Optional[str] = None,
        left: Optional['TreeNode'] = None,
        right: Optional['TreeNode'] = None,
        height: Optional[int] = None,
        members: Optional[Set[str]] = None,
    ):
        self.name = name
        self.left = left
        self.right = right
        self.height = height
        self.members = members if members is not None else set()
        if name:
            self.members.add(name)

    def is_leaf(self) -> bool:
        return self.left is None and self.right is None

    def __repr__(self):
        if self.is_leaf():
            return f"Leaf({self.name})"
        return f"Node(height={self.height}, members={self.members})"

    def to_newick(self) -> str:
        if self.is_leaf():
            return self.name
        left_str = self.left.to_newick() if self.left else ''
        right_str = self.right.to_newick() if self.right else ''
        return f"({left_str},{right_str})"

    def to_newick_with_distances(self, parent_height: Optional[int] = None) -> str:
        if self.is_leaf():
            if parent_height is not None:
                branch_length = int(parent_height)
                return f"{self.name}:{branch_length}"
            else:
                return self.name
        left_str = self.left.to_newick_with_distances(self.height) if self.left else ''
        right_str = self.right.to_newick_with_distances(self.height) if self.right else ''
        if parent_height is not None:
            branch_length = int(parent_height - self.height)
            return f"({left_str},{right_str}):{branch_length}"
        else:
            return f"({left_str},{right_str})"

def build_similarity_tree(
    similarity_scores: Dict[str, int]
) -> TreeNode:
    species = set()
    for key in similarity_scores:
        sp1, sp2 = key.split("_", 1)
        species.add(sp1)
        species.add(sp2)
    clusters: Dict[frozenset, TreeNode] = {
        frozenset([sp]): TreeNode(name=sp) for sp in species
    }

    def cluster_similarity(c1: Set[str], c2: Set[str]) -> int:
        max_sim = None
        for s1 in c1:
            for s2 in c2:
                if s1 == s2:
                    continue
                key = f"{s1}_{s2}" if s1 <= s2 else f"{s2}_{s1}"
                sim = similarity_scores.get(key)
                if sim is not None:
                    if max_sim is None or sim > max_sim:
                        max_sim = sim
        return max_sim if max_sim is not None else float('-inf')

    while len(clusters) > 1:
        cluster_list = list(clusters.keys())
        best_pair = None
        best_score = float('-inf')
        for i in range(len(cluster_list)):
            for j in range(i + 1, len(cluster_list)):
                c1, c2 = cluster_list[i], cluster_list[j]
                sim = cluster_similarity(set(c1), set(c2))
                if sim > best_score:
                    best_score = sim
                    best_pair = (c1, c2)
        if best_pair is None:
            break

        c1, c2 = best_pair
        new_members = set(c1) | set(c2)
        new_node = TreeNode(
            name=None,
            left=clusters[c1],
            right=clusters[c2],
            height=best_score,
            members=new_members,
        )
        del clusters[c1]
        del clusters[c2]
        clusters[frozenset(new_members)] = new_node

    root = next(iter(clusters.values()))
    return root

def get_clusters_at_threshold(node: TreeNode, threshold: int) -> List[List[str]]:
    clusters = []

    def collect(node: TreeNode):
        if node.height is None or node.height <= threshold:
            clusters.append(sorted(list(node.members)))
        else:
            if node.left:
                collect(node.left)
            if node.right:
                collect(node.right)

    collect(node)
    return clusters

def plot_dendrogram(
    root: TreeNode,
    filename: str,
    figsize: Tuple[int, int] = (10, 6)
):
    leaf_names = []
    def get_leaves(node):
        if node.is_leaf():
            leaf_names.append(node.name)
        else:
            if node.left:
                get_leaves(node.left)
            if node.right:
                get_leaves(node.right)
    get_leaves(root)
    y_positions = {name: i for i, name in enumerate(leaf_names)}

    fig, ax = plt.subplots(figsize=figsize)

    def draw_node(node, parent_height=None):
        if node.is_leaf():
            x = 0 if node.height is None else 0
            y = y_positions[node.name]
            ax.text(x - 5, y, node.name, va='center', ha='right', fontsize=10)
            return x, y
        left_x, left_y = draw_node(node.left, node.height)
        right_x, right_y = draw_node(node.right, node.height)
        x = node.height
        ax.plot([x, x], [left_y, right_y], color='k')
        ax.plot([x, left_x], [left_y, left_y], color='k')
        ax.plot([x, right_x], [right_y, right_y], color='k')
        if parent_height is not None:
            ax.plot([x, parent_height], [(left_y + right_y) / 2, (left_y + right_y) / 2], color='k')
        return x, (left_y + right_y) / 2

    draw_node(root)
    ax.set_ylim(-1, len(leaf_names))
    ax.set_xlim(left=0)
    ax.invert_xaxis()
    ax.set_xlabel("Needleman-Wunsch similarity score")
    ax.set_ylabel("Species")
    ax.set_yticks([])
    ax.set_title("Phylogenetic Tree (Dendrogram)")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()